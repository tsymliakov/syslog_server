import socketserver
from concurrent_log_handler import ConcurrentRotatingFileHandler
import logging
import time


logger = logging.getLogger("MultiThreadLogger")
logger.setLevel(logging.INFO)
handler = ConcurrentRotatingFileHandler(f"{__name__}.log",
                                        maxBytes=1024*1024,
                                        backupCount=5)
logger.addHandler(handler)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global logger
        addr = self.client_address
        print(f"Connected to {addr}")

        while True:
            data = self.request.recv(1024).strip()
            if not data:
                print(f"Connection closed by {addr}")
                break

            message = data.decode(encoding="utf-8")
            print(message)
            logger.info(message)

            response = f"Echo: {message}"
            self.request.sendall(response.encode())
            time.sleep(3)

        print(f"Connection closed for {addr}")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    host, port = "localhost", 9999
    with ThreadedTCPServer((host, port), ThreadedTCPRequestHandler) as server:
        print(f"Server started on {host}:{port}")
        server.serve_forever()
