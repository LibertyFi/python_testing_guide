from unittest.mock import MagicMock, Mock, patch

from src.level_4.database import Connection, Database
from src.level_4.interface import ServerInterface
from src.level_4.session import Session


# Sometimes we want to mock an entire class instead of just one instance, so we patch the class and have it return a
# mock instance
@patch("src.level_4.session.ServerInterface")
def test_connect_success(mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = True
    mock_interface_class.return_value = mock_interface
    session = Session()

    connected = session.connect()

    mock_interface.connect_to_server.assert_called_once()

    assert connected


# But we still haven't mocked the database!
# Here's how we can handle a class such as Database, that returns a context manager
@patch("src.level_4.session.ServerInterface")
@patch("src.level_4.session.Db", spec_set=Database)
def test_connect_success_mock_db(mock_db: MagicMock, mock_interface_class: MagicMock) -> None:
    mock_interface = Mock(spec_set=ServerInterface)
    mock_interface.connect_to_server.return_value = True
    mock_interface_class.return_value = mock_interface
    mock_conn = MagicMock(spec_set=Connection)
    mock_db.get.return_value.__enter__.return_value = mock_conn
    session = Session()

    connected = session.connect()

    mock_conn.begin.assert_called_once()
    mock_interface.connect_to_server.assert_called_once()

    assert connected
