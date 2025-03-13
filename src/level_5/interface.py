import logging


class ServerInterface:
    def connect_to_server(self) -> bool:
        logging.info("Called actual connect_to_server")
        return True


class ConnectionCounter:
    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> None:
        self.count += 1
