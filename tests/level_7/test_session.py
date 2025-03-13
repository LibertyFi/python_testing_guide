from unittest.mock import MagicMock, call

import pytest

from src.level_7.interface import ServerInterface
from src.level_7.session import Session


@pytest.fixture
def mock_interface() -> MagicMock:
    mock_interface = MagicMock(spec_set=ServerInterface)
    mock_interface.send_message = MagicMock()
    return mock_interface


# We can check the content of the call to the mock.
def test_send_messages_one_message(mock_interface: MagicMock) -> None:
    session = Session(mock_interface)

    session.send_messages(["Hello, World"])

    mock_interface.send_message.assert_called_once_with("Hello, World")


# In case of multiple calls, we can also check the details of the calls.
def test_send_messages_multiple_messages(mock_interface: MagicMock) -> None:
    session = Session(mock_interface)

    session.send_messages(["Hello, World", "Hello, Universe"])

    # We can check the number of calls to the mock
    assert mock_interface.send_message.call_count == 2
    # We can check the order and content of the calls to the mock
    # You can set the "any_order" flag to True if you don't want to check the order of the calls, the default is False
    mock_interface.send_message.assert_has_calls(
        [
            call("Hello, World"),
            call("Hello, Universe"),
        ]
    )
