from datetime import datetime, timedelta
from enum import Enum
import sys
import math

from decimal import Decimal
from dataclasses import dataclass
from .MetaTrader5 import MetaTrader5 as mt5


NO_VALID_ID = -1
MAX_MSG_LEN = 0xFFFFFF  # 16Mb - 1byte

UNSET_INTEGER = 2**31 - 1
UNSET_DOUBLE = sys.float_info.max
UNSET_LONG = 2**63 - 1
UNSET_DECIMAL = Decimal(2**127 - 1)
DOUBLE_INFINITY = math.inf

INFINITY_STR = "Infinity"

TickerId = int
OrderId = int
TagValueList = list

FaDataType = int
# FaDataTypeEnum = Enum("N/A", "GROUPS", "PROFILES", "ALIASES")


# MarketDataType = int
class MarketDataType(Enum):
    NULL = "N/A"
    REALTIME = "REALTIME"
    FROZEN = "FROZEN"
    DELAYED = "DELAYED"

    def to_str(self) -> str:
        """Returns the string representation of the enum value."""
        return self.value


class PlatformType(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"


Liquidities = int
# LiquiditiesEnum = Enum("None", "Added", "Remove", "RoudedOut")

SetOfString = set
SetOfFloat = set
ListOfOrder = list
ListOfFamilyCode = list
ListOfContractDescription = list
ListOfDepthExchanges = list
ListOfNewsProviders = list
SmartComponentMap = dict
HistogramDataList = list
ListOfPriceIncrements = list
ListOfHistoricalTick = list
ListOfHistoricalTickBidAsk = list
ListOfHistoricalTickLast = list
ListOfHistoricalSessions = list


@dataclass
class BarData:
    time: int
    open_: float
    high: float
    low: float
    close: float
    tick_volume: float
    spread: float
    real_volume: float


@dataclass
class CommissionReport:
    """
    Class describing an commission report's definition.

    """

    execId = ""
    commission = 0.0
    currency = ""
    realizedPNL = 0.0
    yield_ = 0.0
    yieldRedemptionDate = 0  # YYYYMMDD format


def parse_datetime(end_datetime: str, duration_str: str = None):
    end_dt = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")
    if duration_str:
        duration_value, duration_unit = (
            int(duration_str.split()[0]),
            duration_str.split()[1],
        )
        if duration_unit == "M":
            start_dt = end_dt - timedelta(minutes=duration_value)
        elif duration_unit == "D":
            start_dt = end_dt - timedelta(days=duration_value)
        elif duration_unit == "W":
            start_dt = end_dt - timedelta(weeks=duration_value)
        else:
            start_dt = end_dt
        return start_dt
    return end_dt


def get_interval(bar_size_setting: str):
    intervals = {
        "1 sec": 1,
        "5 secs": 5,
        "15 secs": 15,
        "30 secs": 30,
        "1 min": 60,
        "2 mins": 120,
        "3 mins": 180,
        "5 mins": 300,
        "15 mins": 900,
        "30 mins": 1800,
        "1 hour": 3600,
        "1 day": 86400,
    }
    return intervals.get(bar_size_setting, 60)


def get_timeframe(bar_size_setting: str):
    timeframes = {
        "1 sec": mt5.TIMEFRAME_M1,
        "5 secs": mt5.TIMEFRAME_M5,
        "15 secs": mt5.TIMEFRAME_M15,
        "30 secs": mt5.TIMEFRAME_M30,
        "1 min": mt5.TIMEFRAME_H1,
        "2 mins": mt5.TIMEFRAME_H2,
        "3 mins": mt5.TIMEFRAME_H3,
        "5 mins": mt5.TIMEFRAME_H4,
        "15 mins": mt5.TIMEFRAME_D1,
        "30 mins": mt5.TIMEFRAME_W1,
        "1 hour": mt5.TIMEFRAME_MN1,
        "1 day": mt5.TIMEFRAME_MN1,
    }
    return timeframes.get(bar_size_setting, mt5.TIMEFRAME_M1)


def get_tick_flags(tick_type: str):
    tick_flags = {
        "BID_ASK": mt5.COPY_TICKS_INFO,
        "TRADES": mt5.COPY_TICKS_TRADE,
    }
    return tick_flags.get(tick_type, mt5.COPY_TICKS_ALL)


"""
This is the interface that will need to be overloaded by the customer so
that his/her code can receive info from the Terminal.
"""


class TerminalError(Exception):
    pass


class SymbolSelectError(Exception):
    pass


class CodeMsgPair:
    def __init__(self, code, msg):
        self.errorCode = code
        self.errorMsg = msg

    def __str__(self):
        return f"code={self.errorCode}, msg={self.errorMsg}"

    def code(self):
        return self.errorCode

    def msg(self):
        return self.errorMsg


ALREADY_CONNECTED = CodeMsgPair(mt5.RES_S_OK, "Already connected.")
SERVER_CONNECT_FAIL = CodeMsgPair(-1, "Rpyc Server connection failed")
TERMINAL_CONNECT_FAIL = CodeMsgPair(
    mt5.RES_E_INTERNAL_FAIL_INIT, "Terminal initialization failed"
)

UPDATE_TWS = CodeMsgPair(503, "The TWS is out of date and must be upgraded.")

NOT_CONNECTED = CodeMsgPair(504, "Not connected")

UNKNOWN_ID = CodeMsgPair(505, "Fatal Error: Unknown message id.")
UNSUPPORTED_VERSION = CodeMsgPair(506, "Unsupported version")
BAD_LENGTH = CodeMsgPair(507, "Bad message length")
BAD_MESSAGE = CodeMsgPair(508, "Bad message")
SOCKET_EXCEPTION = CodeMsgPair(509, "Exception caught while reading socket - ")
FAIL_CREATE_SOCK = CodeMsgPair(520, "Failed to create socket")
SSL_FAIL = CodeMsgPair(530, "SSL specific error: ")
INVALID_SYMBOL = CodeMsgPair(579, "Invalid symbol in string - ")
