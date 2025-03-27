from unittest.mock import MagicMock, patch

from src.level_1.session import Session


# This test is actually testing both session.connect and interface.connect_to_server
# which means it's not really a unit test
# --8<-- [start:no_mocking]
def test_connect() -> None:
    session = Session()

    result = session.connect()

    assert result


# --8<-- [end:no_mocking]


# Note that we patch in the session module, not the interface module
# Patch where it's used, not where it's defined
# --8<-- [start:with_mock]
@patch("src.level_1.session.connect_to_server")
def test_connect_success(mock_connect_to_server: MagicMock) -> None:
    session = Session()
    mock_connect_to_server.return_value = True

    connected = session.connect()

    # Check that the mock was called by the connect method
    mock_connect_to_server.assert_called_once()

    # Check that the connect method returns the correct value
    assert connected


@patch("src.level_1.session.connect_to_server")
def test_connect_failure(mock_connect_to_server: MagicMock) -> None:
    session = Session()
    mock_connect_to_server.return_value = False

    connected = session.connect()

    mock_connect_to_server.assert_called_once()

    assert not connected


# --8<-- [end:with_mock]
