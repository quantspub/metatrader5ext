from decimal import Decimal
from enum import Enum
import math
import sys

NO_VALID_ID = -1
MAX_MSG_LEN = 0xFFFFFF  # 16Mb - 1byte
UNSET_INTEGER = 2**31 - 1
UNSET_DOUBLE = sys.float_info.max
UNSET_LONG = 2**63 - 1
UNSET_DECIMAL = Decimal(2**127 - 1)
DOUBLE_INFINITY = math.inf

class Mode(Enum):
    """Mode type.
    
    Includes 5 client modes: IPC, RPYC, EA, EA_IPC, and EA_RPYC.

    IPC: Mode for MetaTrader IPC communication on Windows.
    RPYC: Mode for MetaTrader RPYC communication on Linux.
    EA: Mode for EA communication using sockets.
    EA_IPC: Mode for combining EA and IPC communication.
    EA_RPYC: Mode for combining EA and RPYC communication.
    """
    IPC = "IPC"
    RPYC = "RPYC"
    EA = "EA"
    EA_IPC = "EA_IPC"
    EA_RPYC = "EA_RPYC"

    def to_str(self) -> str:
        """Returns the string representation of the enum value."""
        return self.value
    
class PlatformType(Enum):
    """Platform type.
    
    Includes 2 platform types: WINDOWS and LINUX.
    """
    WINDOWS = "Windows"
    LINUX = "Linux"

    def to_str(self) -> str:
        """Returns the string representation of the enum value."""
        return self.value
