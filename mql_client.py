import socket
import threading

class MQL5Client:
    def __init__(self, rest_host='127.0.0.1', rest_port=1111, stream_host='127.0.0.1', stream_port=2222):
        self.rest_host = rest_host
        self.rest_port = rest_port
        self.stream_host = stream_host
        self.stream_port = stream_port
        self.stream_socket = None
        self.running = False

    def send_request(self, command: str) -> str:
        """ Sends a request to the REST server and returns the decoded response. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.rest_host, self.rest_port))
                s.sendall(command.encode('utf-8'))
                response = s.recv(1024)
                return self.decode_string(self.uncompress_string(response))
        except Exception as e:
            return f"Error: {e}"

    def start_streaming(self):
        """ Connects to the streaming server and continuously listens for updates. """
        try:
            self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream_socket.connect((self.stream_host, self.stream_port))
            self.running = True
            threading.Thread(target=self._listen_stream, daemon=True).start()
        except Exception as e:
            print(f"Streaming connection error: {e}")

    def _listen_stream(self):
        """ Internal method to listen for streaming data. """
        try:
            while self.running:
                data = self.stream_socket.recv(1024)
                if data:
                    print("Stream Update:", self.decode_string(self.uncompress_string(data)))
        except Exception as e:
            print(f"Streaming error: {e}")

    def stop_streaming(self):
        """ Stops the streaming connection. """
        self.running = False
        if self.stream_socket:
            self.stream_socket.close()

    def decode_string(self, encoded_bytes: bytes) -> str:
        """ Decodes the received bytes by reversing the shift encoding. """
        return ''.join(chr(b - 42) for b in encoded_bytes)
    
    def uncompress_string(self, compressed_bytes: bytes) -> bytes:
        """ Decompresses a run-length encoded byte sequence. """
        uncompressed = bytearray()
        i = 0
        while i < len(compressed_bytes):
            char = compressed_bytes[i]
            if i + 1 < len(compressed_bytes) and isinstance(compressed_bytes[i+1], int):
                count = compressed_bytes[i+1]
                uncompressed.extend([char] * count)
                i += 2
            else:
                uncompressed.append(char)
                i += 1
        return bytes(uncompressed)

if __name__ == "__main__":
    client = MQL5Client()
    
    # Test REST requests
    print("Checking connection:", client.send_request("F000^1^"))
    print("Fetching account info:", client.send_request("F001^1^"))
    print("Fetching last tick info:", client.send_request("F020^2^"))
    
    # Start streaming updates
    client.start_streaming()
    input("Press Enter to stop streaming...")
    client.stop_streaming()
            
