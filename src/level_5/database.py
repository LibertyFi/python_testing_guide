from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from types import TracebackType


# --8<-- [start:db_logs]
class Connection:
    def begin(self) -> None:
        logging.info("Called actual begin")

    def commit(self) -> None:
        logging.info("Called actual commit")

    # --8<-- [end:db_logs]
    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        pass


class Database:
    @staticmethod
    def get() -> Connection:
        logging.info("Called actual get")
        return Connection()
