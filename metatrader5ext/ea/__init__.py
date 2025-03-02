from metatrader5ext.ea.client import EAClientConfig, EAClient
from metatrader5ext.ea.connection import Connection
from metatrader5ext.ea.errors import ERROR_DICT
from metatrader5ext.ea.models import *
from metatrader5ext.ea.utils import *

# try:
#     from metatrader5ext.ea.data_stream import MetaTrader5Streamer

#     # TODO: Switch Streaming core to MQTT:
#     # https://github.com/eclipse-paho/paho.mqtt.python/
#     # https://en.wikipedia.org/wiki/MQTT
# except ImportError as e:
#     raise ImportError(
#         "Failed to import MetaTrader5Streamer. Ensure that data_stream file exists in the metatrader5ext directory and is properly compiled."
#     ) from e


__all__ = [
    "EAClientConfig",
    "EAClient",
    "Connection",
    "ERROR_DICT",
    # "MetaTrader5Streamer",
]

"""
low level messaging protocol for financial data streaming.

use sockets not websockets
use a custom protocol not FIX
use a custom message format not JSON
"""