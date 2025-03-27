from collections.abc import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.level_5.database import Connection, Database
from src.level_5.interface import ConnectionCounter, ServerInterface
from src.level_5.session import Session


# A fixture can return a mock.
# --8<-- [start:fixture_mock]
@pytest.fixture
def mock_connection_counter() -> Mock:
    return Mock(spec_set=ConnectionCounter)


# --8<-- [end:fixture_mock]


# A fixture can also return a generator, which allows us to use patch.
# --8<-- [start:fixture_patch]
@pytest.fixture
def mock_interface_class() -> Generator[MagicMock, None, None]:
    with patch("src.level_5.session.ServerInterface", spec_set=ServerInterface) as mock:
        yield mock


# --8<-- [end:fixture_patch]


# The autouse flag means that the fixture will be used automatically, without having it as an argument to the test
# function So the mock DB will be called by session.connect instead of the actual one in every test.
# If you disable the autouse flag and run the run the tests with "-v --log-cli-level=INFO", you'll see the logs of the
# calls to the actual DB implementation.
# --8<-- [start:fixture_autouse]
@pytest.fixture(autouse=True)
def mock_db_connection() -> Generator[tuple[MagicMock, MagicMock], None, None]:
    with patch("src.level_5.session.Db", spec=Database) as mock_db:
        mock_conn = MagicMock(spec_set=Connection)
        mock_db.get.return_value.__enter__.return_value = mock_conn
        yield mock_db, mock_conn


# --8<-- [end:fixture_autouse]


# No need to define the mocks for this test, we just reference the fixtures.
# The mock_db_connection is used automatically, no need to pass it as an argument.
# --8<-- [start:fixture_first_use]
def test_connect_success(mock_interface_class: MagicMock, mock_connection_counter: Mock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = True
    mock_interface_class.return_value = mock_interface
    session = Session(mock_connection_counter)

    connected = session.connect()

    mock_interface.connect_to_server.assert_called_once()
    mock_connection_counter.increment.assert_called_once()

    assert connected


# --8<-- [end:fixture_first_use]


# Thanks to the fixtures, we don't need to repeat the mock setup code, we can reuse them in every test that needs them.
# --8<-- [start:fixture_second_use]
def test_connect_failure(mock_interface_class: MagicMock, mock_connection_counter: Mock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = False
    mock_interface_class.return_value = mock_interface
    session = Session(mock_connection_counter)

    connected = session.connect()

    mock_interface.connect_to_server.assert_called_once()
    mock_connection_counter.increment.assert_not_called()

    assert not connected


# --8<-- [end:fixture_second_use]


# Here we pass the mock_db_connection fixture as an explicit argument so that we can reference the mock in the test, to
# check a call for instance.
# --8<-- [start:fixture_explicit_use]
def test_connect_success_mock_db(
    mock_interface_class: MagicMock, mock_connection_counter: Mock, mock_db_connection: tuple[MagicMock, MagicMock]
) -> None:
    _, mock_conn = mock_db_connection
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = True
    mock_interface_class.return_value = mock_interface
    session = Session(mock_connection_counter)

    connected = session.connect()

    mock_conn.begin.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_interface.connect_to_server.assert_called_once()
    mock_connection_counter.increment.assert_called_once()

    assert connected


# --8<-- [end:fixture_explicit_use]
