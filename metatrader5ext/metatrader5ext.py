import platform
import logging
import queue
import socket
import sys
import threading
import numpy as np
from datetime import datetime, timezone
from typing import Any, Callable, List, Optional, Union
from dataclasses import dataclass
from metatrader5ext.metatrader5 import RpycConfig, MetaTrader5
from metatrader5ext.ea import EAClientConfig, EAClient
from metatrader5ext.common import Mode, PlatformType
from metatrader5ext.errors import ErrorInfo, TerminalError
from metatrader5ext.logging import Logger as MTLogger


@dataclass
class MetaTrader5ExtConfig:
    """
    Configuration for MetaTrader5Ext.

    Parameters:
        id (int): ID of the client. Default is 1.
        mode (Mode): Mode of the client. Default is Mode.IPC.
        market_data (MarketData): Type of market data. Default is MarketData.NULL.
        ea_client (Optional[EAClientConfig]): Configuration for EAClient. Default is None.
        rpyc (Optional[RpycConfig]): Configuration for RPYC. Default is None.
        logger (Optional[Callable]): A logger instance for logging messages. Default is None.
    """
    id: int = 1
    mode: Mode = Mode.IPC
    ea_client: Optional[EAClientConfig] = None
    rpyc: Optional[RpycConfig] = None
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
        _ea_client (EAClient): Server for handling data streams.
        enable_stream (bool): Flag to enable or disable streaming.
        connected (bool): Connection status.
        connection_time (Optional[float]): Time of the connection.
        client_id (Optional[int]): ID of the client.
    """

    (DISCONNECTED, CONNECTING, CONNECTED, REDIRECT) = range(4)
    
    _mt5: Optional[Union[MetaTrader5.MetaTrader5, MetaTrader5]] = None
    _ea_client: Optional[EAClient] = None
    _platform: Optional[PlatformType] = None
    logger: Optional[logging.Logger] = None

    def __init__(self, config: MetaTrader5ExtConfig):
        self._platform = PlatformType(platform.system().capitalize())
        self.logger = (
            config.logger if config.logger else MTLogger(__class__.__name__)
        )
        self._msg_queue = queue.Queue()
        self._lock = threading.Lock()
        self._is_stream = False
        self.connected = False
        self.connection_time = None
        self._conn_state = None
        self._terminal_version = None
        self._id = config.id
        self._config = config
        self._ea_config: Optional[EAClientConfig] = None

        try:
            self._initialize_mt5(config)
        except Exception as e:
            self.logger.error(f"Failed to initialize MetaTrader5: {e}")
            raise RuntimeError(
                "Error occurred while trying to connect to the MetaTrader instance."
            )

    def __del__(self):
        """
        Destructor to ensure cleanup.

        Resets the connection and state.
        """
        self.disconnect()
        
        self.connected = False
        self.client_id = None
        self._terminal_version = None
        self.connection_time = None
        self._conn_state = MetaTrader5Ext.DISCONNECTED
        self._mt5 = None
        self._ea_client = None
        self._msg_queue = queue.Queue()

    def _initialize_mt5(self, config: MetaTrader5ExtConfig):
        if config.mode == Mode.IPC or config.mode == Mode.RPYC:
            self._mt5 = self._initialize_mt_client(config)
        elif config.mode == Mode.EA:
            if config.ea_client is not None:
                self._ea_client = self._initialize_ea_client(config)
            else:
                raise RuntimeError("EA configuration is required for EA mode.")
        elif config.mode == Mode.EA_IPC or config.mode == Mode.EA_RPYC:
            self._mt5 = self._initialize_mt_client(config)
            if config.ea_client is not None:
                self._ea_client = self._initialize_ea_client(config)
        else:
            raise ValueError("Invalid mode selected.")

    def _initialize_mt_client(self, config: MetaTrader5ExtConfig):
        if config.mode == Mode.IPC:
            return MetaTrader5
        elif config.mode == Mode.RPYC:
            if config.rpyc is not None:
                return MetaTrader5.MetaTrader5(
                    host=config.rpyc.host,
                    port=config.rpyc.port,
                    keep_alive=config.rpyc.keep_alive,
                )
            else:
                raise RuntimeError("RPYC configuration is required for RPYC mode.")
        else:
            raise ValueError("Invalid mode for MT client initialization.")

    def _initialize_ea_client(self, config: MetaTrader5ExtConfig):
        self._is_stream = config.ea_client.enable_stream
        self._ea_config = EAClientConfig(
            host=config.ea_client.host,
            rest_port=config.ea_client.rest_port,
            stream_port=config.ea_client.stream_port,
            encoding=config.ea_client.encoding,
            use_socket=config.ea_client.use_socket,
            enable_stream=config.ea_client.enable_stream,
            callback=config.ea_client.callback,
            debug=config.ea_client.debug,
        )
        return EAClient(config=self._ea_config)

    def is_connected(self) -> bool:
        """
        Checks if the connection to the MetaTrader 5 terminal is active.

        Returns:
            bool: True if connected, False otherwise.
        """
        return MetaTrader5Ext.CONNECTED == self._conn_state and self.connected

    def get_error(self) -> ErrorInfo:
        """
        Retrieves the last error from the MetaTrader 5 terminal.

        Returns:
            Optional[ErrorInfo]: The last error code and message.
        """

        if not self.is_connected() or self._mt5 is None:
            self.logger.debug("not connected to terminal")
            return ErrorInfo(0, "MetaTrader5 instance is not initialized")

        code, msg = self._mt5.last_error()
        if code == self._mt5.RES_E_INTERNAL_FAIL_INIT:
            return ErrorInfo(code, f"Terminal initialization failed: {msg}")

        return ErrorInfo(code, msg)

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
            self.send_msg((0, self._mt5.terminal_info()))
            self.managed_accounts()

        except TerminalError as e:
            TERMINAL_CONNECT_FAIL._msg += f" => {e.__str__()}"
            self.logger.error(
                NO_VALID_ID,
                TERMINAL_CONNECT_FAIL.code(),
                TERMINAL_CONNECT_FAIL.msg(),
            )
        except socket.error as e:
            SERVER_CONNECT_FAIL._msg += f" => {e.__str__()}"
            self.logger.error(
                NO_VALID_ID, SERVER_CONNECT_FAIL.code(), SERVER_CONNECT_FAIL.msg()
            )

    def disconnect(self):
        """
        Disconnects from the MetaTrader 5 terminal.
        """
        with self._lock:
            self.logger.debug("disconnecting")
            if self._mt5 is not None:
                self._mt5.shutdown()

            if self._ea_client is not None:
                self._ea_client = None

            self.logger.debug("Connection closed")

    def get_conn_state(self):
        """
        Retrieves the current connection state.

        Returns:
            int: The current connection state.
        """
        return self._conn_state

    def set_conn_state(self, state: int):
        """
        Sets the connection state.

        Parameters:
            state (int): The new connection state.
        """
        self._conn_state = state

    def managed_accounts(self):
        """
        Retrieves and logs the managed accounts.
        """
        account_info = self._mt5.account_info()
        self.connected_server = account_info.server
        self.logger.info(f"{self.is_connected()} | {self.connected_server}")
        accounts = tuple([f"{account_info.login}"])
        self.send_msg((0, accounts))

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
        if self._ea_client:
            self._ea_client.start_stream(callback)
            self.logger.info(f"Subscribed to symbols: {symbols} with req_id: {req_id}")

    def unsubscribe(self, req_id: str, symbols: List[str]):
        """
        Unsubscribes from streaming data for the specified symbols.

        Parameters:
            req_id (str): Request ID for the subscription.
            symbols (List[str]): List of symbols to unsubscribe from.
        """
        if self._ea_client:
            self._ea_client.stop_stream()
            self.logger.info(
                f"Unsubscribed from symbols: {symbols} with req_id: {req_id}"
            )
