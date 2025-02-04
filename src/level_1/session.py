from src.level_1.interface import connect_to_server


class Session:
    def connect(self) -> bool:
        return connect_to_server()
