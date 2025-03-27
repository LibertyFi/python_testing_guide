from collections.abc import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.level_6.interface import ServerInterface
from src.level_6.session import Session


# --8<-- [start:mock_interface_class]
@pytest.fixture
def mock_interface_class() -> Generator[MagicMock, None, None]:
    with patch("src.level_6.session.ServerInterface", spec_set=ServerInterface) as mock:
        yield mock


# --8<-- [end:mock_interface_class]


# Let's mock the sleep function to avoid waiting for what could be a long time during testing.
# --8<-- [start:mock_sleep]
@pytest.fixture
def mock_sleep() -> Generator[MagicMock, None, None]:
    with patch("src.level_6.session.time.sleep") as mock:
        yield mock


# --8<-- [end:mock_sleep]


# To test the start method, we need to mock the connect method, otherwise we're also testing it.
# The side_effect argument allows us to
# - mock the return value of the function for each successive call.
# - have the mock call a function everytime the mock is called.
# --8<-- [start:with_side_effect]
def test_start_success(mock_sleep: MagicMock, mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.is_server_connected.side_effect = [True, True, False]
    mock_interface_class.return_value = mock_interface
    mock_sleep.return_value = None
    session = Session()

    def connect() -> None:
        session.connected = True

    session.connect = MagicMock(side_effect=connect)

    session.start()

    session.connect.assert_called_once()
    assert mock_interface.is_server_connected.call_count == 3


# --8<-- [end:with_side_effect]


# Without setting the side_effect, the mock of session.connect doesn't do anything, so connected is never set.
# --8<-- [start:without_side_effect]
def test_start_not_connected(mock_sleep: MagicMock, mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface_class.return_value = mock_interface
    mock_sleep.return_value = None
    session = Session()
    session.connect = MagicMock()

    session.start()

    session.connect.assert_called_once()
    mock_interface.is_server_connected.assert_not_called()


# --8<-- [end:without_side_effect]
