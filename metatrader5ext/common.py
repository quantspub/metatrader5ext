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
    
    Includes 3 client modes: IPC, EA, and EA_IPC.

    IPC: Mode for MetaTrader IPC communication on Windows.
    EA: Mode for EA communication using sockets.
    EA_IPC: Mode for combining EA and IPC communication (EA for streaming and IPC for request-reply).
    
    Since RPYC is used for IPC communication in Linux, it will be used for IPC mode in Linux (MetaTrader RPYC communication on Linux).
    """
    IPC = "IPC"
    EA = "EA"
    EA_IPC = "EA_IPC"

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
