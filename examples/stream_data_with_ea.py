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

import asyncio
from metatrader5ext.ea.client import EAClient

def handle_stream_data(data: str) -> None:
    """Callback function to handle received streaming data."""
    print("Streamed data:", data)

async def main():
    client = EAClient()

    # Start streaming updates
    client.start_stream(callback=handle_stream_data)
    input("Press Enter to stop streaming...")
    client.stop_stream()

if __name__ == "__main__":
    asyncio.run(main())
