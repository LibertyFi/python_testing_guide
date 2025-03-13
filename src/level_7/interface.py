import logging


class ServerInterface:
    def send_message(self, message: str) -> None:
        logging.info(f"Calling actual send_message with {message}")
