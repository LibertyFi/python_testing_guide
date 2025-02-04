from unittest.mock import Mock

from src.level_2.interface import ServerInterface
from src.level_2.session import Session


# The easiest way to use a Mock
def test_connect_success() -> None:
    interface = Mock()
    interface.connect_to_server.return_value = True
    session = Session(interface)
    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# The downside is that Mock generates attributes on the fly
# so you can use attributes that don't even exist on the original object
def test_connect_success_shouldnt_be_allowed() -> None:
    interface = Mock()
    interface.connect_to_server.return_value = True
    # This doesn't raise an error, but it shouldn't be possible
    interface.not_an_actual_attribute = "This shouldn't be possible"
    session = Session(interface)
    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# You should use spec_set to specify what the Mock is supposed to mock
def test_connect_success_spec_set() -> None:
    interface = Mock(spec_set=ServerInterface)
    interface.connect_to_server.return_value = True
    # This raises an AttributeError
    # interface.not_an_actual_attribute = "This shouldn't be possible"  # noqa: ERA001
    session = Session(interface)
    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected
