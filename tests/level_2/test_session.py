from unittest.mock import Mock

from src.level_2.interface import ServerInterface
from src.level_2.session import Session


# The easiest way to use Mock to mock an object
def test_connect_success() -> None:
    interface = Mock()
    interface.connect_to_server.return_value = True
    session = Session(interface)

    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# The downside is that Mock generates attributes on the fly so you can use attributes that don't even exist on the
# original object
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


# Instance attributes are not part of the class spec, so they don't exist as far as spec_set is concerned
def test_connect_success_spec_set_instance_attribute() -> None:
    interface = Mock(spec_set=ServerInterface)
    interface.connect_to_server.return_value = True
    # This works as expected
    interface.class_attribute = "This is a class attribute"
    # This raises an AttributeError
    # interface.instance_attribute = "This attribute doesn't exist when the mock is created"  # noqa: ERA001
    session = Session(interface)

    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# If you need to mock an instance attribute (or any attribute that is defined at runtime), you can use spec instead of
# spec_set; beware that this is not as strict as spec_set, it will simply ensure that an attribute can't be accessed
# if it has not been set.
def test_connect_success_simple_spec_for_instance_attribute() -> None:
    interface = Mock(spec=ServerInterface)
    interface.connect_to_server.return_value = True
    interface.class_attribute = "This is a class attribute"
    # Now this works
    interface.instance_attribute = "This is an instance attribute"
    # But this will still raise an AttributeError
    # logging.info(f"This shouldn't be possible: {interface.unexisting_instance_attribute}")  # noqa: ERA001
    session = Session(interface)

    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected


# You can also define the mock and its attributes at the same time if you prefer the one-liner syntax.
def test_connect_success_simple_spec_one_liner() -> None:
    interface = Mock(
        spec=ServerInterface,
        class_attribute="This is a class attribute",
        instance_attribute="This is an instance attribute",
        connect_to_server=Mock(return_value=True),
    )
    session = Session(interface)

    connected = session.connect()

    interface.connect_to_server.assert_called_once()

    assert connected
