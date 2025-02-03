import pytest

from src.calculator import add, divide, multiply, subtract


def test_operations():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

    assert subtract(5, 2) == 3
    assert subtract(0, 1) == -1

    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0

    assert divide(6, 2) == 3
    with pytest.raises(ValueError):
        divide(6, 0)


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 1) == -1


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0


def test_divide_valid():
    assert divide(6, 2) == 3
    assert divide(-6, 2) == -3


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(6, 0)
