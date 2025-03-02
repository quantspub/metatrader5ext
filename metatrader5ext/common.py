from datetime import datetime, timedelta
from enum import Enum
import sys
import math

from decimal import Decimal
from dataclasses import dataclass



class ClientMode(Enum):
    """Client mode type.
    
    Includes 3 client modes: IPC, SOCKETS, and RPYC.
    """
    IPC = "IPC"
    SOCKETS = "SOCKETS"
    RPYC = "RPYC"

    def to_str(self) -> str:
        """Returns the string representation of the enum value."""
        return self.value
    
class MarketDataType(Enum):
    """Market data type.
    
    Includes 4 market data types: NULL, REALTIME, FROZEN, and DELAYED.
    """
    NULL = "N/A"
    REALTIME = "REALTIME"
    FROZEN = "FROZEN"
    DELAYED = "DELAYED"

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
    
class ModuleType(Enum):
    """Module type.
    
    Includes 2 module types: MT and EA.
    """
    MT = "MT"
    EA = "EA"

    def to_str(self) -> str:
        """Returns the string representation of the enum value."""
        return self.value
    

