import asyncio
from metatrader5ext.ea.client import EAClient

if __name__ == "__main__":
    client = EAClient()

    async def main():
        # Test REST requests
        await client.check_connection()
        print("Fetching static account info:", await client.get_static_account_info())
        print("Fetching dynamic account info:", await client.get_dynamic_account_info())
        print("Fetching last tick info:", await client.get_last_tick_info())
        print("Fetching broker server time:", await client.get_broker_server_time())
        print("Fetching instrument info:", await client.get_instrument_info())

        # Start streaming updates
        client.start_streaming()
        input("Press Enter to stop streaming...")
        client.stop_streaming()

    asyncio.run(main())