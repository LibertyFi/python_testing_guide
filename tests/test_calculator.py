import pytest

from src.calculator import add, divide, multiply, subtract


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
