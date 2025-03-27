from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from src.level_3.interface import ServerInterface
from src.level_3.session import Session


# Sometimes a simple Mock is not enough to mock something
# --8<-- [start:missing_magic_method]
def test_connect_success_missing_magic_method() -> None:
    interface = Mock(spec_set=ServerInterface)
    session = Session(interface)
    # This raises a TypeError because Mock doesn't implement the magic/special __add__ method so it can't effectively
    # mock an int
    # session.active_connections = Mock()  # noqa: ERA001

    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# --8<-- [end:missing_magic_method]


# MagicMock gets rid of that problem by automatically implementing the magic/special methods
# --8<-- [start:magic_mock]
def test_connect_success_magic() -> None:
    interface = Mock(spec_set=ServerInterface)
    session = Session(interface)
    # This works as expected because MagicMock automatically implements the magic/special methods, including __add__
    session.active_connections = MagicMock()

    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# --8<-- [end:magic_mock]


# Mock also can't be used to mock async functions, we need to use AsyncMock
# Note the special decorator as well (requires pytest-asyncio on top of pytest)
# --8<-- [start:async_mock]
@pytest.mark.asyncio
async def test_aconnect_async_mock() -> None:
    interface = Mock(spec_set=ServerInterface)
    # This raises a TypeError because the mock will simply return a boolean instead of a coroutine
    # interface.aconnect_to_server.return_value = True  # noqa: ERA001
    # We need to use AsyncMock to mock the async function properly
    interface.aconnect_to_server = AsyncMock(return_value=True)
    session = Session(interface)

    connected = await session.aconnect()

    # We could use assert_called_once() as well, but assert_awaited_once() is more specific
    interface.aconnect_to_server.assert_awaited_once()

    assert connected


# --8<-- [end:async_mock]
