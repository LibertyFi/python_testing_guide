from src.calculator import add, divide, multiply, subtract


def test_operations():
  assert add(2, 3) == 5
  assert add(-1, 1) == 0

  assert subtract(5, 2) == 3
  assert subtract(0, 1) == -1

  assert multiply(2, 3) == 6
  assert multiply(0, 5) == 0

  assert divide(6, 2) == 3
  try:
      divide(6, 0)
  except ValueError:
      pass