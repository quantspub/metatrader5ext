"""
Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""


"""
Just a thin wrapper around a socket.
It allows us to keep some other info along with it.
"""


import socket
import threading
import logging
import sys
from ibapi.errors import FAIL_CREATE_SOCK
from ibapi.errors import CONNECT_FAIL
from ibapi.common import NO_VALID_ID


#TODO: support SSL !!

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.wrapper = None
        self.lock = threading.Lock()

    def connect(self):
        try:
            self.socket = socket.socket()
        #TODO: list the exceptions you want to catch
        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, FAIL_CREATE_SOCK.code(), FAIL_CREATE_SOCK.msg())

        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, CONNECT_FAIL.code(), CONNECT_FAIL.msg())

        self.socket.settimeout(1)   #non-blocking

    def disconnect(self):
        self.lock.acquire()
        try:
            if self.socket is not None:
                logger.debug("disconnecting")
                self.socket.close()
                self.socket = None
                logger.debug("disconnected")
                if self.wrapper:
                    self.wrapper.connectionClosed()
        finally:
            self.lock.release()

    def isConnected(self):
        return self.socket is not None

    def sendMsg(self, msg):
        logger.debug("acquiring lock")
        self.lock.acquire()
        logger.debug("acquired lock")
        if not self.isConnected():
            logger.debug("sendMsg attempted while not connected, releasing lock")
            self.lock.release()
            return 0
        try:
            nSent = self.socket.send(msg)
        except socket.error:
            logger.debug("exception from sendMsg %s", sys.exc_info())
            raise
        finally:
            logger.debug("releasing lock")
            self.lock.release()
            logger.debug("release lock")

        logger.debug("sendMsg: sent: %d", nSent)

        return nSent

    def recvMsg(self):
        if not self.isConnected():
            logger.debug("recvMsg attempted while not connected, releasing lock")
            return b""
        try:
            buf = self._recvAllMsg()
            # receiving 0 bytes outside a timeout means the connection is either
            # closed or broken
            if len(buf) == 0:
                logger.debug("socket either closed or broken, disconnecting")
                self.disconnect()
        except socket.timeout:
            logger.debug("socket timeout from recvMsg %s", sys.exc_info())
            buf = b""
        except socket.error:
            logger.debug("socket broken, disconnecting")
            self.disconnect()
            buf = b""
        except OSError:
            # Thrown if the socket was closed (ex: disconnected at end of script) 
            # while waiting for self.socket.recv() to timeout.
            logger.debug("Socket is broken or closed.")

        return buf

    def _recvAllMsg(self):
        cont = True
        allbuf = b""

        while cont and self.isConnected():
            buf = self.socket.recv(4096)
            allbuf += buf
            logger.debug("len %d raw:%s|", len(buf), buf)

            if len(buf) < 4096:
                cont = False

        return allbuf

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

