from enum import Enum

class Mode(Enum):
    """Mode type.
    
    Includes 3 client modes: IPC, RPYC, and EA.

    IPC: Mode for MetaTrader IPC communication on Windows.
    RPYC: Mode for MetaTrader RPYC communication on Linux.
    EA: Mode for EA communication using sockets.
    """
    IPC = "IPC"
    RPYC = "RPYC"
    EA = "EA"

    def to_str(self) -> str:
        """Returns the string representation of the enum value."""
        return self.value
    
class MarketData(Enum):
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
