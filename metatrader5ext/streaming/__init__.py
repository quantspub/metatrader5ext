try:
    from metatrader5ext.streaming.data_stream import MetaTrader5Streamer

    # TODO: Switch Streaming core to MQTT:
    # https://github.com/eclipse-paho/paho.mqtt.python/
    # https://en.wikipedia.org/wiki/MQTT
except ImportError as e:
    raise ImportError(
        "Failed to import MetaTrader5Streamer. Ensure that data_stream file exists in the metatrader5ext directory and is properly compiled."
    ) from e


__all__ = [
    "MetaTrader5Streamer",
]
