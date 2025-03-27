import time

from src.level_6.interface import ServerInterface


class Session:
    interface: ServerInterface
    connected: bool

    def __init__(self) -> None:
        self.interface = ServerInterface()
        self.connected = False

    def connect(self) -> None:
        self.connected = self.interface.connect_to_server()

    def start(self) -> None:
        self.connect()
        if not self.connected:
            return
        while self.interface.is_server_connected():
            time.sleep(1)
