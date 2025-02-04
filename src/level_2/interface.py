import logging


class ServerInterface:
    def __init__(self) -> None:
        pass

    def connect_to_server(self) -> bool:
        logging.info("Called actual connect_to_server")
        return True
