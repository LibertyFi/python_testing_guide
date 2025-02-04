from src.level_2.interface import ServerInterface


class Session:
    interface: ServerInterface

    def __init__(self, interface: ServerInterface) -> None:
        self.interface = interface

    def connect(self) -> bool:
        return self.interface.connect_to_server()
