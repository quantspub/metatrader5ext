from dataclasses import dataclass

@dataclass 
class RpycConfig:
    """
    Configuration for RPYC.

    Parameters:
        host (str): Host address for the RPYC connection. Default is "localhost".
        port (int): Port number for the RPYC connection. Default is 18812.
        keep_alive (bool): Whether to keep the RPYC connection alive. Default is False.
    """
    host: str = "localhost"
    port: int = 18812
    keep_alive: bool = False