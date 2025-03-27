from src.level_5.database import Database as Db
from src.level_5.interface import ConnectionCounter, ServerInterface


class Session:
    interface: ServerInterface

    def __init__(self, connection_counter: ConnectionCounter) -> None:
        self.interface = ServerInterface()
        self.connection_counter = connection_counter

    def connect(self) -> bool:
        with Db.get() as conn:
            conn.begin()
            # TODO: write some data to the database
            conn.commit()
        connected = self.interface.connect_to_server()
        if connected:
            self.connection_counter.increment()
        return connected
