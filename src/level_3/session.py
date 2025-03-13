from src.level_3.interface import ServerInterface


class Session:
    interface: ServerInterface
    active_connections: int = 0

    def __init__(self, interface: ServerInterface) -> None:
        self.interface = interface

    def connect(self) -> bool:
        self.active_connections += 1
        return self.interface.connect_to_server()

    async def aconnect(self) -> bool:
        self.active_connections += 1
        return await self.interface.aconnect_to_server()
