import logging


class ServerInterface:
    def connect_to_server(self) -> bool:
        logging.info("Called actual connect_to_server")
        return True

    def is_server_connected(self) -> bool:
        logging.info("Called actual is_server_connected")
        return True
