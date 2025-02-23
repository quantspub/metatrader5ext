import asyncio
from connection import Connection
from errors import ERROR_DICT

class EAClient(Connection):
    def __init__(self):
        super().__init__()
        self.debug = False

    async def check_connection(self):
        message = 'F000^1^'
        self.command_return_error = ''

        try:
            ok, data_string = await self.send_message(message)
            if not ok:
                self.command_ok = False
                return False

            if self.debug:
                print(data_string)

            return self._process_connection_response(data_string)
        except Exception as error:
            self.command_return_error = ERROR_DICT['00001']
            self.command_ok = False
            raise Exception(f"Connection check failed: {error}")

    def _process_connection_response(self, data_string):
        x = data_string.split('^')
        if x[1] == 'OK':
            self.timeout = False
            self.command_ok = True
            return True
        else:
            self.timeout = True
            self.command_return_error = ERROR_DICT['99900']
            self.command_ok = True
            return False

    def get_static_account_info(self):
        """ Fetches the static account information from the MetaTrader 5 EA. """
        return "Account Info: Balance=10000, Equity=10000, Free Margin=10000"
    
    def get_dynamic_account_info(self):
        """ Fetches the dynamic account information from the MetaTrader 5 EA. """
        return "Account Info: Balance=10000, Equity=10000, Free Margin=10000"


if __name__ == "__main__":
    client = EAClient()
    
    # Test REST requests
    print("Checking connection:", client.check_connection())
    # print("Fetching static account info:", client.get_static_account_info())   
    # print("Fetching dynamic account info:", client.get_dynamic_account_info())
    # print("Fetching last tick info:", client.get_last_tick_info())

#     # Start streaming updates
#     client.start_streaming()
#     input("Press Enter to stop streaming...")
#     client.stop_streaming()