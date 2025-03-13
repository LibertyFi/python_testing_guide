import logging


class ServerInterface:
    class_attribute = "This is a class attribute"

    def __init__(self) -> None:
        self.instance_attribute = "This is an instance attribute"

    def connect_to_server(self) -> bool:
        logging.info("Called actual connect_to_server")
        return True

    async def aconnect_to_server(self) -> bool:
        logging.info("Called actual aconnect_to_server")
        return True
