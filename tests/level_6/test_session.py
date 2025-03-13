from collections.abc import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.level_6.interface import ServerInterface
from src.level_6.session import Session


@pytest.fixture
def mock_interface_class() -> Generator[MagicMock, None, None]:
    with patch("src.level_6.session.ServerInterface", spec_set=ServerInterface) as mock:
        yield mock


# Let's mock the sleep function to avoid waiting for what could be a long time during testing.
@pytest.fixture
def mock_sleep() -> Generator[MagicMock, None, None]:
    with patch("src.level_6.session.time.sleep") as mock:
        yield mock


# Use pytest.raises to check that a specific exception is raised by the code under test.
def test_connect_failure(mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = False
    mock_interface_class.return_value = mock_interface
    session = Session()

    # The match argument allows us to check that the exception message matches a specific regex pattern.
    with pytest.raises(ConnectionError, match="Failed to connect to server"):
        session.connect()

    mock_interface.connect_to_server.assert_called_once()


def test_connect_success(mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = True
    mock_interface_class.return_value = mock_interface
    session = Session()

    session.connect()

    mock_interface.connect_to_server.assert_called_once()

    assert session.connected


# To test the start method, we need to mock the connect method, otherwise we're also testing it.
# The side_effect argument allows us to
# - mock the return value of the function for each successive call.
# - have the mock call a function everytime the mock is called.
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


# Without setting the side_effect, the mock of session.connect doesn't do anything, so connected is never set.
def test_start_not_connected(mock_sleep: MagicMock, mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface_class.return_value = mock_interface
    mock_sleep.return_value = None
    session = Session()
    session.connect = MagicMock()

    session.start()

    session.connect.assert_called_once()
    mock_interface.is_server_connected.assert_not_called()
