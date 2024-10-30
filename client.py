import socket
import datetime
from threading import Thread


def tcp_client():
    for _ in range(5):
        host = '127.0.0.1'
        port = 9999

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((host, port))
            print("Соединение открыто")

            message = str(datetime.datetime.now())
            client_socket.sendall(message.encode(encoding="utf-8"))

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            client_socket.close()
            print("Соединение закрыто")


if __name__ == "__main__":
    threads = []
    for _ in range(10):
        threads.append(Thread(target=tcp_client))

    for thread in threads:
        thread.run()
