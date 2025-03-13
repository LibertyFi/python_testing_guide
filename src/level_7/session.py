from src.level_7.interface import ServerInterface


class Session:
    interface: ServerInterface

    def __init__(self, interface: ServerInterface) -> None:
        self.interface = interface

    def send_messages(self, messages: list[str]) -> None:
        for message in messages:
            self.interface.send_message(message)
