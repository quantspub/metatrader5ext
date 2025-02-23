import asyncio
from .connection import Connection
from .errors import ERROR_DICT

class EAClient(Connection):
    def __init__(self, host: str = '127.0.0.1', rest_port: int = 15556, stream_port: int = 15557, encoding: str = 'utf-8', debug: bool = False):
        super().__init__(host, rest_port, stream_port, encoding, debug)

    def _process_response(self, response, expected_code):
        x = response.split('^')
        if x[0] == expected_code:
            self.timeout = False
            self.command_ok = True
            return x
        else:
            self.timeout = True
            self.command_return_error = ERROR_DICT['99900']
            self.command_ok = True
            return None

    async def check_connection(self):
        message = 'F000^1^'
        self.command_return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.command_ok = False
                return False

            if self.debug:
                print(response)

            return self._process_response(response, 'F000') is not None
        except Exception as error:
            self.command_return_error = ERROR_DICT['00001']
            self.command_ok = False
            raise Exception(f"Connection check failed: {error}")

    async def get_static_account_info(self):
        message = 'F001^1^'
        self.command_return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.command_ok = False
                return None

            if self.debug:
                print(response)

            x = self._process_response(response, 'F001')
            if x:
                return {
                    "name": x[2],
                    "login": x[3],
                    "currency": x[4],
                    "type": x[5],
                    "leverage": x[6],
                    "trade_allowed": x[7],
                    "limit_orders": x[8],
                    "margin_call": x[9],
                    "margin_close": x[10],
                    "company": x[11]
                }
            return None
        except Exception as error:
            self.command_return_error = ERROR_DICT['00001']
            self.command_ok = False
            raise Exception(f"Failed to get static account info: {error}")

    async def get_dynamic_account_info(self):
        message = 'F002^1^'
        self.command_return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.command_ok = False
                return None

            if self.debug:
                print(response)

            x = self._process_response(response, 'F002')
            if x:
                return {
                    "balance": x[2],
                    "equity": x[3],
                    "profit": x[4],
                    "margin": x[5],
                    "margin_level": x[6],
                    "margin_free": x[7]
                }
            return None
        except Exception as error:
            self.command_return_error = ERROR_DICT['00001']
            self.command_ok = False
            raise Exception(f"Failed to get dynamic account info: {error}")

    async def get_last_tick_info(self, instrument_name='EURUSD'):
        message = f'F020^2^{instrument_name}^'
        self.command_return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.command_ok = False
                return None

            if self.debug:
                print(response)

            x = self._process_response(response, 'F020')
            if x:
                return {
                    "instrument": instrument_name,
                    "date": int(x[2]),
                    "ask": float(x[3]),
                    "bid": float(x[4]),
                    "last": float(x[5]),
                    "volume": int(x[6]),
                    "spread": float(x[7]),
                    "date_in_ms": int(x[8])
                }
            return None
        except Exception as error:
            self.command_return_error = ERROR_DICT['00001']
            self.command_ok = False
            raise Exception(f"Failed to get last tick info: {error}")

    # Add more methods as needed...

if __name__ == "__main__":
    client = EAClient()
    
    # Test REST requests
    asyncio.run(client.check_connection())
    # print("Fetching static account info:", asyncio.run(client.get_static_account_info()))   
    # print("Fetching dynamic account info:", asyncio.run(client.get_dynamic_account_info()))
    # print("Fetching last tick info:", asyncio.run(client.get_last_tick_info()))

#     # Start streaming updates
#     client.start_streaming()
#     input("Press Enter to stop streaming...")
#     client.stop_streaming()