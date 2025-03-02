import platform

# import importlib.util
import sys
import os
from .config import RpycConfig

current_dir = os.path.dirname(__file__)
try:
    if platform.system() == "Windows":
        import MetaTrader5 as MetaTrader5

        # MetaTrader5 = importlib.import_module("MetaTrader5")
    else:
        sys.path.insert(0, current_dir)
        try:
            from . import MetaTrader5 as MetaTrader5

            # MetaTrader5 = importlib.import_module(
            #     ".MetaTrader5", package="metatrader5ext"
            # )
        except ImportError:
            raise ImportError("MetaTrader5 is not available on this system.")
except ImportError as e:
    raise ImportError(f"Failed to import MetaTrader5: {e}")
finally:
    if current_dir in sys.path:
        sys.path.remove(current_dir)


try:
    from metatrader5ext.metatrader5.terminal import (
        ContainerStatus,
        DockerizedMT5TerminalConfig,
        DockerizedMT5Terminal,
        ContainerExists,
        NoContainer,
        UnknownContainerStatus,
        TerminalLoginFailure,
    )
except ImportError as e:
    raise ImportError(
        "Failed to import DockerizedMT5Terminal. Ensure that terminal file exists"
    ) from e

__all__ = [
    "MetaTrader5",
    "RpycConfig",
    "DockerizedMT5TerminalConfig",
    "DockerizedMT5Terminal",
    "ContainerStatus",
    "ContainerExists",
    "NoContainer",
    "UnknownContainerStatus",
    "TerminalLoginFailure",
]
