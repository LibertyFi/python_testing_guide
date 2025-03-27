from src.level_8.interface import ServerInterface


class SessionError(Exception):
    pass


class Session:
    interface: ServerInterface
    connected: bool

    def __init__(self) -> None:
        self.interface = ServerInterface()
        self.connected = False
        self.ignore_connection_errors = False

    def connect(self) -> None:
        try:
            self.connected = self.interface.connect_to_server()
        except ConnectionError:
            self.connected = False
        if not self.connected and not self.ignore_connection_errors:
            msg = "Failed to connect to server"
            raise SessionError(msg)
