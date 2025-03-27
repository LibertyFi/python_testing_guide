from collections.abc import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.level_8.interface import ServerInterface
from src.level_8.session import Session, SessionError


# --8<-- [start:mock_interface_class]
@pytest.fixture
def mock_interface_class() -> Generator[MagicMock, None, None]:
    with patch("src.level_8.session.ServerInterface", spec_set=ServerInterface) as mock:
        yield mock


# --8<-- [end:mock_interface_class]


# Use side_effect have a mock raise an exception.
# --8<-- [start:caught_exception]
def test_connect_interface_exception(mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.side_effect = ConnectionError("Failed to connect to server")
    mock_interface_class.return_value = mock_interface
    session = Session()
    session.ignore_connection_errors = True

    session.connect()

    mock_interface.connect_to_server.assert_called_once()

    assert not session.connected


# --8<-- [end:caught_exception]


# Use pytest.raises to check that a specific exception is raised by the code under test.
# --8<-- [start:raised_exception]
def test_connect_session_exception(mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = False
    mock_interface_class.return_value = mock_interface
    session = Session()

    # The match argument allows us to check that the exception message matches a specific regex pattern.
    with pytest.raises(SessionError, match="Failed to connect to server"):
        session.connect()

    mock_interface.connect_to_server.assert_called_once()


# --8<-- [end:raised_exception]
