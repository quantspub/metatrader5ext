from enum import Enum

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
