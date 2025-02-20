"""
    This script demonstrates how to stream data using WebSockets and MetaTrader 5.

    The script connects to a WebSocket server and listens for incoming messages.
    It also initializes and configures the MetaTrader5Ext API to connect to the MetaTrader 5 terminal,
    start the API, and subscribe to streaming data for the specified symbols.

    Functions:
        listen(): Asynchronously listens for messages from the WebSocket server.
        main(): Configures and initializes MetaTrader5Ext, connects to the MetaTrader 5 terminal,
                subscribes to streaming data, and starts listening to WebSocket messages.
"""

import asyncio
import websockets
import time
from metatrader5ext import MetaTrader5Ext, MetaTrader5ExtConfig


async def listen():
    uri = "ws://127.0.0.1:15558"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")
        try:
            async for message in websocket:
                print("Received message:", message)
        except websockets.ConnectionClosed as e:
            print("Connection closed:", e)


def main():
    # Configuration for MetaTrader5Ext
    config = MetaTrader5ExtConfig(stream_debug=True, stream_use_websockets=True)

    # Initialize MetaTrader5Ext
    mt5_ext = MetaTrader5Ext(config)

    try:
        # Connect to MetaTrader 5 terminal
        mt5_ext.connect()

        # Start the API
        mt5_ext.start_api()

        # Subscribe to streaming data
        mt5_ext.subscribe(req_id="1", symbols=["EURUSD"], interval=1.0, callback=None)

        # Start listening to WebSocket messages
        asyncio.get_event_loop().run_until_complete(listen())

    except Exception as e:
        print("Error:", e)
    finally:
        # Ensure the streamer is stopped
        mt5_ext.unsubscribe(req_id="1", symbols=["EURUSD"])
        mt5_ext.disconnect()


if __name__ == "__main__":
    main()
