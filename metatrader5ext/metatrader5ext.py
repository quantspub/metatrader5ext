import platform
import logging
import queue
import socket
import sys
import threading
import numpy as np
from datetime import datetime, timezone
from typing import Any, Callable, List, Optional
from dataclasses import dataclass
from .metatrader5 import MetaTrader5
from .ea import EAClientConfig, EAClient
from .common import ModuleType, ClientMode, MarketDataType, PlatformType
# from .utils import ClientException, current_fn_name

# from .common import (
#     PlatformType,
#     MarketDataType,
#     NO_VALID_ID,
#     TERMINAL_CONNECT_FAIL,
#     SERVER_CONNECT_FAIL,
#     TerminalError,
#     CodeMsgPair,
#     BarData,
#     TickerId,
# )

@dataclass 
class RpycConfig:
    """
    Configuration for RPYC.

    Parameters:
        host (str): Host address for the RPYC connection. Default is "localhost".
        port (int): Port number for the RPYC connection. Default is 18812.
        keep_alive (bool): Whether to keep the RPYC connection alive. Default is False.
    """
    host: str = "localhost"
    port: int = 18812
    keep_alive: bool = False

@dataclass
class MetaTrader5ExtConfig:
    """
    Configuration for MetaTrader5Ext.

    Parameters:
        client_id (int): ID of the client. Default is 1.
        module (ModuleType): Type of module. Default is ModuleType.MT.
        mode (ClientMode): Mode of the client. Default is ClientMode.IPC.
        market_data_type (MarketDataType): Type of market data. Default is MarketDataType.NULL.
        ea_client_config (Optional[EAClientConfig]): Configuration for EAClient. Default is None.
        rpyc_config (Optional[RpycConfig]): Configuration for RPYC. Default is None.
        logger (Optional[Callable]): A logger instance for logging messages. Default is None.
    """
    client_id: int = 1
    module: ModuleType = ModuleType.MT
    mode: ClientMode = ClientMode.IPC
    market_data_type: MarketDataType = MarketDataType.NULL
    ea_client_config: Optional[EAClientConfig] = None
    rpyc_config: Optional[RpycConfig] = None
    logger: Optional[Callable] = None


class MetaTrader5Ext:
    """
    MetaTrader5 Wrapper.

    Parameters:
        config (MetaTrader5ExtConfig): Configuration object for MetaTrader5Ext.

    Attributes:
        logger (Callable): Logger instance for logging messages.
        _msg_queue (queue.Queue): Queue for managing messages.
        _lock (threading.Lock): Lock for thread-safe operations.
        _mt5 (MetaTrader5): MetaTrader5 instance.
        _stream_manager (MetaTrader5Streamer): Server for handling data streams.
        stream_interval (float): Interval for streaming data.
        enable_stream (bool): Flag to enable or disable streaming.
        connected (bool): Connection status.
        connection_time (Optional[float]): Time of the connection.
        conn_state (Optional[int]): State of the connection.
        _terminal_version (Optional[int]): Version of the terminal.
        client_id (Optional[int]): ID of the client.
        market_data_type (MarketDataType): Type of market data.
    """
    
    (DISCONNECTED, CONNECTING, CONNECTED, REDIRECT) = range(4)
    
    _mt5: Optional[MetaTrader5] = None
    _stream_manager: Optional[MetaTrader5Streamer] = None
    _platform: Optional[PlatformType] = None
    logger: Optional[logging.Logger] = None
    client_id: int = 1
    market_data_type: MarketDataType = MarketDataType.NULL

    def __init__(self, config: MetaTrader5ExtConfig):
        self._platform = PlatformType(platform.system().capitalize())
        self.logger = (
            config.logger if config.logger else logging.getLogger(__class__.__name__)
        )
        self._msg_queue = queue.Queue()
        self._lock = threading.Lock()
        self.enable_stream = config.enable_stream

        try:
            self._initialize_mt5(config)
        except Exception as e:
            self.logger.error(f"Failed to initialize MetaTrader5: {e}")
            raise RuntimeError(
                "Error occurred while trying to connect to the MetaTrader instance."
            )

        if self.enable_stream:
            self._initialize_stream_manager(config)

        self.connected = False
        self.connection_time = None
        self._conn_state = None
        self._terminal_version = None
        self.client_id = config.client_id
        self.market_data_type = config.market_data_type
        self.config = config

    def _initialize_mt5(self, config: MetaTrader5ExtConfig):
        if self._platform == PlatformType.WINDOWS:
            self._mt5 = MetaTrader5
        else:
            self._mt5 = MetaTrader5.MetaTrader5(
                host=config.rpyc_host,
                port=config.rpyc_port,
                keep_alive=config.rpyc_keep_alive,
            )

    def _initialize_stream_manager(self, config: MetaTrader5ExtConfig):
        self._stream_manager = EAClient(
            host=config.stream_host,
            stream_port=config.stream_callback_port,
            ws_port=config.stream_ws_port,
            callback=config.stream_callback,
            stream_interval=config.stream_interval,
            use_socket=config.stream_use_socket,
            use_websockets=config.stream_use_websockets,
            debug=config.stream_debug,
        )
        self._stream_manager.start()

    def is_connected(self):
        """
        Checks if the connection to the MetaTrader 5 terminal is active.

        Returns:
            bool: True if connected, False otherwise.
        """
        return MetaTrader5Ext.CONNECTED == self._conn_state and self.connected

    def get_connection_time(self):
        """
        Retrieves the connection time.

        Returns:
            Optional[float]: The connection time as a timestamp.
        """
        return self.connection_time

    def get_error(self) -> Optional[CodeMsgPair]:
        """
        Retrieves the last error from the MetaTrader 5 terminal.

        Returns:
            Optional[CodeMsgPair]: The last error code and message.
        """
        if not self.is_connected():
            self.logger.debug("not connected to terminal")
            return None

        code, msg = self._mt5.last_error()
        if code == self._mt5.RES_E_INTERNAL_FAIL_INIT:
            return CodeMsgPair(code, f"Terminal initialization failed: {msg}")

        return CodeMsgPair(code, msg)

    def set_conn_state(self, conn_state):
        """
        Sets the connection state.

        Parameters:
            conn_state (int): The new connection state.
        """
        _conn_state = self.conn_state
        self.conn_state = conn_state
        self.logger.debug(
            "%s conn_state: %s -> %s" % (id(self), _conn_state, self.conn_state)
        )

    def reset(self):
        """
        Resets the connection and streaming state.
        """
        self.connected = False
        self.client_id = None
        self._terminal_version = None
        self.connection_time = None
        self.conn_state = None
        self.enable_stream = False
        if self._stream_manager:
            self._stream_manager.stop()
            self._stream_manager = None
        self._msg_queue = queue.Queue()
        self.market_data_type = MarketDataType.NULL
        self.set_conn_state(MetaTrader5Ext.DISCONNECTED)

    #
    # Messaging Queue
    #
    def send_msg(self, msg: Any):
        """
        Sends a message to the MetaTrader 5 terminal.

        Parameters:
            msg (Any): The message to send.

        Returns:
            int: The number of bytes sent.
        """
        self.logger.debug("acquiring lock")
        with self._lock:
            self.logger.debug("acquired lock")
            if not self.is_connected():
                self.logger.debug(
                    "send_msg attempted while not connected, releasing lock"
                )
                return 0
            try:
                self._msg_queue.put_nowait(msg)
                nSent = len(msg)
            except socket.error:
                self.logger.debug("exception from send_msg %s", sys.exc_info())
                raise
            finally:
                self.logger.debug("releasing lock")

        self.logger.debug("send_msg: sent: %d", nSent)
        return nSent

    def recv_msg(self):
        """
        Receives a message from the MetaTrader 5 terminal.

        Returns:
            Any: The received message.
        """
        if not self.is_connected():
            self.logger.debug("recv_msg attempted while not connected")
            return None

        eval_result = None
        try:
            msg = self._msg_queue.get()
            self.logger.debug(f"Received message of type {type(msg).__name__}: {msg}")

            if isinstance(msg, str):
                if "get_connection_time" in msg:
                    eval_result = self.connection_time
                else:
                    eval_result = self._mt5.eval(msg)
            else:
                eval_result = msg

            self._msg_queue.task_done()
        except socket.timeout:
            self.logger.debug("socket timeout from recv_msg %s", sys.exc_info())
        except socket.error:
            self.logger.debug("socket either closed or broken, disconnecting")
            self.disconnect()

        return eval_result

    #
    # Connection
    #
    def connect(self, path: str = "", **kwargs):
        """
        Connects to the MetaTrader 5 terminal.

        Parameters:
            path (str): Path to the MetaTrader 5 terminal EXE file.
            **kwargs: Additional arguments for the MetaTrader 5 connection.
        """
        try:
            self.connected = self._mt5.initialize(path, **kwargs)
            if not self.connected:
                TERMINAL_CONNECT_FAIL = self.get_error()
                raise TerminalError(TERMINAL_CONNECT_FAIL)

            self.connection_time = datetime.now(timezone.utc).timestamp()
            self.send_msg((0, current_fn_name(), self._mt5.terminal_info()))

        except TerminalError as e:
            TERMINAL_CONNECT_FAIL.errorMsg += f" => {e.__str__()}"
            self.logger.error(
                NO_VALID_ID,
                TERMINAL_CONNECT_FAIL.code(),
                TERMINAL_CONNECT_FAIL.msg(),
            )
        except socket.error as e:
            SERVER_CONNECT_FAIL.errorMsg += f" => {e.__str__()}"
            self.logger.error(
                NO_VALID_ID, SERVER_CONNECT_FAIL.code(), SERVER_CONNECT_FAIL.msg()
            )

    def disconnect(self):
        """
        Disconnects from the MetaTrader 5 terminal.
        """
        with self._lock:
            self.logger.debug("disconnecting")
            self._mt5.shutdown()
            self.logger.debug("Connection closed")
            self.reset()

    #
    # Client
    #
    def start_api(self):
        """
        Check the Initialized terminal connection after connecting to rpyc socket.
        """

        if not self.is_connected():
            text = f"MetaTrader5 initialization failed, error = {self.get_error()}"
            self.logger.error(text)
            raise ClientException(
                TERMINAL_CONNECT_FAIL.code(), TERMINAL_CONNECT_FAIL.msg(), text
            )

        self.req_ids()
        self.managed_accounts()

    def managed_accounts(self):
        """
        Retrieves and logs the managed accounts.
        """
        account_info = self._mt5.account_info()
        self.connected_server = account_info.server
        self.logger.info(f"{self.is_connected()} | {self.connected_server}")
        accounts = tuple([f"{account_info.login}"])
        self.send_msg((0, current_fn_name(), accounts))

    def req_ids(self):
        """
        Generates a valid ID.
        """
        ids = np.random.randint(10000, size=1)
        self.send_msg((0, current_fn_name(), ids.tolist()))

    def req_market_data_type(self, market_data_type: MarketDataType):
        """
        Requests the market data type.

        Parameters:
            market_data_type (MarketDataType): The market data type to request.
        """
        self.market_data_type = market_data_type
        self.send_msg((0, current_fn_name(), self.market_data_type.value))
        return None

    def subscribe(
        self,
        req_id: str,
        symbols: List[str],
        interval: float,
        callback: Callable,
        **kwargs,
    ):
        """
        Subscribes to streaming data for the specified symbols.

        Parameters:
            req_id (str): Request ID for the subscription.
            symbols (List[str]): List of symbols to subscribe to.
            interval (float): Interval in seconds for data streaming.
            callback (Callable): Callback function to handle the streamed data.
            **kwargs: Additional arguments for the callback.
        """
        if self._stream_manager:
            if self.config.stream_use_socket:
                self._stream_manager.set_callback(callback)
            else:
                self._stream_manager.create_streaming_task(
                    req_id, symbols, interval, callback, kwargs
                )
            self._stream_manager.start()
            self.logger.info(f"Subscribed to symbols: {symbols} with req_id: {req_id}")

    def unsubscribe(self, req_id: str, symbols: List[str]):
        """
        Unsubscribes from streaming data for the specified symbols.

        Parameters:
            req_id (str): Request ID for the subscription.
            symbols (List[str]): List of symbols to unsubscribe from.
        """
        if self._stream_manager:
            if not self.config.stream_use_socket:
                self._stream_manager.stop_streaming_task(req_id, symbols)

            self._stream_manager.stop()
            self.logger.info(
                f"Unsubscribed from symbols: {symbols} with req_id: {req_id}"
            )
``` 
