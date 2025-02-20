"""
    This script demonstrates how to stream data using the MetaTrader5Ext API with callbacks.

    Functions:
        handle_data(data): Callback function to handle received streaming data.

    Configuration:
        MetaTrader5ExtConfig: Configuration for MetaTrader5Ext with specified callback, debug mode, and websocket usage.

    Usage:
        - Connects to the MetaTrader 5 terminal.
        - Starts the MetaTrader5Ext API.
        - Subscribes to streaming data for specified symbols and interval.
        - Continuously receives and handles streaming data using the callback function.
        - Ensures proper cleanup by unsubscribing and disconnecting in case of errors or termination.
"""

import time
from metatrader5ext import MetaTrader5Ext, MetaTrader5ExtConfig


def handle_data(data):
    print("Received data:", data)


# Configuration for MetaTrader5Ext
config = MetaTrader5ExtConfig(
    stream_callback=handle_data, stream_debug=True, stream_use_websockets=False
)

# Initialize MetaTrader5Ext
mt5_ext = MetaTrader5Ext(config)

try:
    # Connect to MetaTrader 5 terminal
    mt5_ext.connect()

    # Start the API
    mt5_ext.start_api()

    # Subscribe to streaming data
    mt5_ext.subscribe(
        req_id="1", symbols=["EURUSD"], interval=1.0, callback=handle_data
    )

    while True:
        time.sleep(1)
except Exception as e:
    print("Error:", e)
finally:
    # Ensure the streamer is stopped
    mt5_ext.unsubscribe(req_id="1", symbols=["EURUSD"])
    mt5_ext.disconnect()
