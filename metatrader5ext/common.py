from enum import Enum

class Mode(Enum):
    """Mode type.
    
    Includes 3 client modes: MT_IPC, MT_RPYC, and EA_SOCKETS.

    MT_IPC: Mode for MetaTrader IPC communication on Windows.
    MT_RPYC: Mode for MetaTrader RPYC communication on Linux.
    EA_SOCKETS: Mode for EA communication using sockets.
    """
    MT_IPC = "MT_IPC"
    MT_RPYC = "MT_RPYC"
    EA_SOCKETS = "EA_SOCKETS"

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
