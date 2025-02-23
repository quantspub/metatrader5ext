import socket
import threading
import asyncio
from typing import Optional, Callable

class Connection:
    host: str
    rest_port: int
    stream_port: int
    stream_socket: Optional[socket.socket]
    running: bool
    encoding: str
    stream_callback: Optional[Callable[[str], None]]
    debug: bool

    def __init__(self, host: str = '127.0.0.1', rest_port: int = 15556, stream_port: int = 15557, encoding: str = 'utf-8', debug: bool = False) -> None:
        self.host = host
        self.rest_port = rest_port
        self.stream_port = stream_port
        self.stream_socket = None
        self.running = False
        self.encoding = encoding
        self.stream_callback = None
        self.debug = debug

    async def send_message(self, message: str) -> str:
        """ Sends a request command/message to the REST server and returns the decoded response. """
        loop = asyncio.get_event_loop()
        try:
            reader, writer = await asyncio.open_connection(self.host, self.rest_port, loop=loop)
            writer.write(message.encode(self.encoding))
            await writer.drain()
            response = await reader.read(1024)
            writer.close()
            await writer.wait_closed()
            if self.debug:
                print(f"Sent: {message}, Received: {response.decode(self.encoding)}")
            return response.decode(self.encoding)
        except Exception as e:
            if self.debug:
                print(f"Error: {e}")
            return f"Error: {e}"

    def start_streaming(self, callback: Optional[Callable[[str], None]] = None) -> None:
        """ Connects to the streaming server and continuously listens for updates. """
        self.stream_callback = callback
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
                    decoded_data = data.decode(self.encoding)
                    if self.debug:
                        print(f"Stream Update: {decoded_data}")
                    if self.stream_callback:
                        self.stream_callback(decoded_data)
        except Exception as e:
            print(f"Streaming error: {e}")

    def stop_streaming(self) -> None:
        """ Stops the streaming connection. """
        self.running = False
        if self.stream_socket:
            self.stream_socket.close()

