import socket
import threading

class Connection:
    def __init__(self, host='127.0.0.1', rest_port=15556, stream_port=15557):
        self.host = host
        self.rest_port = rest_port
        self.stream_port = stream_port
        self.stream_socket = None
        self.running = False

    def send_request(self, command: str) -> str:
        """ Sends a request to the REST server and returns the decoded response. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.rest_port))
                s.sendall(command.encode('utf-8'))
                response = s.recv(1024)
                return response.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"

    def start_streaming(self):
        """ Connects to the streaming server and continuously listens for updates. """
        try:
            self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream_socket.connect((self.host, self.stream_port))
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
                    print("\nStream Update:", data.decode('utf-8'))
        except Exception as e:
            print(f"Streaming error: {e}")

    def stop_streaming(self):
        """ Stops the streaming connection. """
        self.running = False
        if self.stream_socket:
            self.stream_socket.close()

if __name__ == "__main__":
    client = Connection()
    
    # Test REST requests
    print("Checking connection:", client.send_request("F000^1^"))
    print("Fetching account info:", client.send_request("F001^1^"))
    print("Fetching last tick info:", client.send_request("F020^2^"))
    
    # Start streaming updates
    client.start_streaming()
    input("Press Enter to stop streaming...")
    client.stop_streaming()

