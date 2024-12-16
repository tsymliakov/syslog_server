import argparse
import configparser
import logging
import signal
import socketserver
import sys

from concurrent_log_handler import ConcurrentRotatingFileHandler


config = configparser.ConfigParser()
config.read("config.ini")


logger = logging.getLogger("MultiThreadLogger")
logger.setLevel(logging.INFO)
handler = ConcurrentRotatingFileHandler(
    f"{__name__}.log", maxBytes=1024 * 1024, backupCount=5
)
logger.addHandler(handler)


class SyslogServer(socketserver.ThreadingUDPServer):
    def __init__(self, server_address, request_handler_class):
        super().__init__(server_address, request_handler_class)
        signal.signal(signal.SIGTERM, self._handle_sigterm)

    def _handle_sigterm(self, sig, frame):
        self.stop()

    def start(self):
        try:
            logger.info(
                f"Syslog server started on {self.server_address[0]}:{self.server_address[1]}"
            )
            self.serve_forever(poll_interval=0.5)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.shutdown()
        self.server_close()
        logger.info(
            f"Syslog server on {self.server_address[0]}:{self.server_address[1]} stopped"
        )


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip(), encoding="utf-8")
        logger.info(f"{self.client_address[0]}: {str(data.encode('utf-8'))}")


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--start", help="Start syslog server.", action="store_true"
    )
    return parser


if __name__ == "__main__":
    parser = set_args()
    args = parser.parse_args()

    if not args.start:
        parser.print_help()
        sys.exit()

    server = SyslogServer(
        (config.get("Server", "host"),
         config.getint("Server", "port")),
        SyslogUDPHandler
    )

    server.start()
