import asyncio
from typing import Optional, Dict, Any
from .connection import Connection
from .errors import ERROR_DICT

class EAClient(Connection):
    """
    Extends the Connection class to provide specific methods for interacting with the EA server.

    Attributes:
        return_error (str): Stores the error message for the last command.
        ok (bool): Indicates if the last command was successful.
    """
    def __init__(self, host: str = '127.0.0.1', rest_port: int = 15556, stream_port: int = 15557, encoding: str = 'utf-8', debug: bool = False) -> None:
        super().__init__(host, rest_port, stream_port, encoding, debug)
        self.return_error = ''
        self.ok = False

    def _process_response(self, response: str, expected_code: str) -> Optional[Dict[str, Any]]:
        """
        Processes the server response and checks if it matches the expected code.

        :param response: The server response string.
        :param expected_code: The expected response code.
        :return: A dictionary of response parts if the response matches the expected code, otherwise None.
        """
        parsed_response = self.parse_response_message(response)
        if 'error' in parsed_response:
            if self.debug:
                print(parsed_response)

            self.timeout = True
            self.return_error = ERROR_DICT['99900']
            self.ok = False
            return None
        
        if parsed_response['command'] != expected_code:
            self.timeout = True
            self.return_error = ERROR_DICT['99900']
            self.ok = False
            return None

        self.timeout = False
        self.ok = True
        return parsed_response

    async def check_connection(self) -> bool:
        """
        Checks the connection to the server.

        :return: True if the connection is successful, otherwise False.
        """
        message = self.make_message('F000', '1', [])
        self.return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.ok = False
                return False

            if self.debug:
                print(response)

            return self._process_response(response, 'F000') is not None
        except Exception as error:
            self.return_error = ERROR_DICT['00001']
            self.ok = False
            raise Exception(f"Connection check failed: {error}")

    async def get_static_account_info(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves static account information from the server.

        :return: A dictionary containing static account information if successful, otherwise None.
        """
        message = self.make_message('F001', '1', [])
        self.return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.ok = False
                return None

            if self.debug:
                print(response)

            parsed_response = self._process_response(response, 'F001')
            if parsed_response:
                return {
                    "name": parsed_response['data'][0],
                    "login": parsed_response['data'][1],
                    "currency": parsed_response['data'][2],
                    "type": parsed_response['data'][3],
                    "leverage": parsed_response['data'][4],
                    "trade_allowed": parsed_response['data'][5],
                    "limit_orders": parsed_response['data'][6],
                    "margin_call": parsed_response['data'][7],
                    "margin_close": parsed_response['data'][8],
                    "company": parsed_response['data'][9]
                }
            return None
        except Exception as error:
            self.return_error = ERROR_DICT['00001']
            self.ok = False
            raise Exception(f"Failed to get static account info: {error}")

    async def get_dynamic_account_info(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves dynamic account information from the server.

        :return: A dictionary containing dynamic account information if successful, otherwise None.
        """
        message = self.make_message('F002', '1', [])
        self.return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.ok = False
                return None

            if self.debug:
                print(response)

            parsed_response = self._process_response(response, 'F002')
            if parsed_response:
                return {
                    "balance": parsed_response['data'][0],
                    "equity": parsed_response['data'][1],
                    "profit": parsed_response['data'][2],
                    "margin": parsed_response['data'][3],
                    "margin_level": parsed_response['data'][4],
                    "margin_free": parsed_response['data'][5]
                }
            return None
        except Exception as error:
            self.return_error = ERROR_DICT['00001']
            self.ok = False
            raise Exception(f"Failed to get dynamic account info: {error}")

    async def get_last_tick_info(self, instrument_name: str = 'EURUSD') -> Optional[Dict[str, Any]]:
        """
        Retrieves the last tick information for a given instrument.

        :param instrument_name: The name of the instrument.
        :return: A dictionary containing the last tick information if successful, otherwise None.
        """
        message = self.make_message('F020', '2', [instrument_name])
        self.return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.ok = False
                return None

            if self.debug:
                print(response)

            parsed_response = self._process_response(response, 'F020')
            if parsed_response:
                return {
                    "instrument": instrument_name,
                    "date": int(parsed_response['data'][0]),
                    "ask": float(parsed_response['data'][1]),
                    "bid": float(parsed_response['data'][2]),
                    "last": float(parsed_response['data'][3]),
                    "volume": int(parsed_response['data'][4]),
                    "spread": float(parsed_response['data'][5]),
                    "date_in_ms": int(parsed_response['data'][6])
                }
            return None
        except Exception as error:
            self.return_error = ERROR_DICT['00001']
            self.ok = False
            raise Exception(f"Failed to get last tick info: {error}")

    async def get_broker_server_time(self) -> Optional[Dict[str, int]]:
        """
        Retrieves the broker server time.

        :return: A dictionary containing the broker server time if successful, otherwise None.
        """
        message = self.make_message('F005', '1', [])
        self.return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.ok = False
                return None

            if self.debug:
                print(response)

            parsed_response = self._process_response(response, 'F005')
            if parsed_response:
                y = parsed_response['data'][0].split('-')
                my_date = {
                    "year": int(y[0]),
                    "month": int(y[1]),
                    "day": int(y[2]),
                    "hour": int(y[3]),
                    "minute": int(y[4]),
                    "second": int(y[5])
                }
                return my_date
            return None
        except Exception as error:
            self.return_error = ERROR_DICT['00001']
            self.ok = False
            raise Exception(f"Failed to get broker server time: {error}")

    async def get_instrument_info(self, instrument_name: str = 'EURUSD') -> Optional[Dict[str, Any]]:
        """
        Retrieves information about a specific instrument.

        :param instrument_name: The name of the instrument.
        :return: A dictionary containing the instrument information if successful, otherwise None.
        """
        message = self.make_message('F003', '2', [instrument_name])
        self.return_error = ''

        try:
            response = await self.send_message(message)
            if not response:
                self.ok = False
                return None

            if self.debug:
                print(response)

            parsed_response = self._process_response(response, 'F003')
            if parsed_response:
                return {
                    "instrument": instrument_name,
                    "digits": parsed_response['data'][0],
                    "max_lotsize": parsed_response['data'][1],
                    "min_lotsize": parsed_response['data'][2],
                    "lot_step": parsed_response['data'][3],
                    "point": parsed_response['data'][4],
                    "tick_size": parsed_response['data'][5],
                    "tick_value": parsed_response['data'][6],
                    "swap_long": parsed_response['data'][7],
                    "swap_short": parsed_response['data'][8],
                    "stop_level": parsed_response['data'][9],
                    "contract_size": parsed_response['data'][10]
                }
            return None
        except Exception as error:
            self.return_error = ERROR_DICT['00001']
            self.ok = False
            raise Exception(f"Failed to get instrument info: {error}")

    # Add more methods as needed...