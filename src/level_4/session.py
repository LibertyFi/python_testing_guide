from src.level_4.database import Database as Db
from src.level_4.interface import ServerInterface


class Session:
    interface: ServerInterface

    def __init__(self) -> None:
        self.interface = ServerInterface()

    def connect(self) -> bool:
        with Db.get() as conn:
            conn.begin()
            # TODO: write some data to the database
            conn.commit()

        return self.interface.connect_to_server()
