import pytest

from src.level_0.calculator import add, divide, multiply, subtract


# This test is too complicated, it tests too many things
# --8<-- [start:too_complicated]
def test_operations() -> None:
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

    assert subtract(5, 2) == 3
    assert subtract(0, 1) == -1

    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0

    assert divide(6, 2) == 3
    with pytest.raises(ValueError, match="divide by zero"):
        divide(6, 0)


# --8<-- [end:too_complicated]


# Instead, we should split it into proper unit tests: each one tests one unit of code
# --8<-- [start:split]
def test_add() -> None:
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract() -> None:
    assert subtract(5, 2) == 3
    assert subtract(0, 1) == -1


def test_multiply() -> None:
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0


def test_divide_valid() -> None:
    assert divide(6, 2) == 3
    assert divide(-6, 2) == -3


def test_divide_by_zero() -> None:
    with pytest.raises(ValueError, match="divide by zero"):
        divide(6, 0)


# --8<-- [end:split]
