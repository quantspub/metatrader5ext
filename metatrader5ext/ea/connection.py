import socket
import threading
from typing import Optional

class Connection:
    host: str
    rest_port: int
    stream_port: int
    stream_socket: Optional[socket.socket]
    running: bool

    def __init__(self, host: str = '127.0.0.1', rest_port: int = 15556, stream_port: int = 15557) -> None:
        self.host = host
        self.rest_port = rest_port
        self.stream_port = stream_port
        self.stream_socket = None
        self.running = False

    def send_mesaage(self, message: str) -> str:
        """ Sends a request message/command to the REST server and returns the decoded response. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.rest_port))
                s.sendall(message.encode('utf-8'))
                response = s.recv(1024)
                return response.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"

    def start_streaming(self) -> None:
        """ Connects to the streaming server and continuously listens for updates. """
        try:
            self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream_socket.connect((self.host, self.stream_port))
            self.running = True
            threading.Thread(target=self._listen_stream, daemon=True).start()
        except Exception as e:
            print(f"Streaming connection error: {e}")

    def _listen_stream(self) -> None:
        """ Internal method to listen for streaming data. """
        try:
            while self.running:
                data = self.stream_socket.recv(1024)
                if data:
                    print("\nStream Update:", data.decode('utf-8'))
                    # can use a callback here
                    # callback(data.decode('utf-8'))
        except Exception as e:
            print(f"Streaming error: {e}")

    def stop_streaming(self) -> None:
        """ Stops the streaming connection. """
        self.running = False
        if self.stream_socket:
            self.stream_socket.close()

