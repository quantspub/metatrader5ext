"""
MetaTrader5 Client Extension

This module provides a client for interacting with MetaTrader 5. It supports both request-reply and streaming data functionalities.

The MetaTrader5 module is used for request-reply interactions with the MetaTrader 5 terminal, allowing you to perform operations such as placing orders, retrieving account information, and more.

For streaming data from MetaTrader 5, use the streaming module, which provides real-time data feeds and updates.

Usage:
    import MetaTrader5 as mt5

    # Initialize the MetaTrader 5 terminal
    mt5.initialize()

    # Perform operations
    account_info = mt5.account_info()
    print(account_info)

    # Shutdown the MetaTrader 5 terminal
    mt5.shutdown()

Example for using MetaTrader5Streamer:
    from metatrader5ext import MetaTrader5Streamer

    def handle_data(data):
        print("Received data:", data)

    streamer = MetaTrader5Streamer(callback=handle_data, debug=True)
    streamer.start()

    # Stop the streamer
    if streamer.is_running():
        streamer.stop()
    
    # Non-socket data retrieval - Calls the symbol_info_tick function every 0.025 seconds
    streamer = MetaTrader5Streamer(callback=handle_data, use_socket=False, debug=True)
    streamer.start()
    # Create a streaming task
    streamer.create_streaming_task("req1", ["EURUSD", "GBPUSD"], 1.0, mt5.symbol_info_tick)

    # Stop the streaming task after some time
    import time
    time.sleep(10)
    streamer.stop_streaming_task("req1", ["EURUSD", "GBPUSD"])
    
    if streamer.is_running():
        streamer.stop()
"""

from rpyc.utils.classic import DEFAULT_SERVER_PORT as RPYC_DEFAULT_SERVER_PORT
from metatrader5ext.metatrader5 import MetaTrader5, RpycConfig, DockerizedMT5Terminal, DockerizedMT5TerminalConfig
from metatrader5ext.ea import EAClient, EAClientConfig
from metatrader5ext.metatrader5ext import MetaTrader5Ext, MetaTrader5ExtConfig
from metatrader5ext.timeframe_agg import TimeframeAggregator
from metatrader5ext.logging import Logger as MTLogger
from metatrader5ext.common import *
from metatrader5ext.errors import *

__all__ = [
    "MetaTrader5ExtConfig",
    "MetaTrader5Ext",
    "DockerizedMT5TerminalConfig",
    "DockerizedMT5Terminal",
    "RpycConfig",
    "MetaTrader5",
    "EAClient",
    "TimeframeAggregator",
    "MTLogger",
    "RPYC_DEFAULT_SERVER_PORT",
]
