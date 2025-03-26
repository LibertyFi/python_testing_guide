# Welcome to the Python unit tests tutorial

## Prerequisites

- Python 3.11+
- pytest installed as a dev dependency

## What Unit Tests Are For

1. **Detecting Bugs Early**: Unit tests catch errors and bugs in specific functions or methods before they become larger issues in the overall system.
2. **Ensuring Code Quality**: They validate that the code behaves as intended, improving reliability.
3. **Facilitating Refactoring**: With a suite of unit tests, you can confidently make changes to your codebase knowing that tests will alert you if something breaks.
4. **Documenting Behavior**: Tests serve as documentation by illustrating how functions or methods are intended to work.
5. **Improving Development Speed**: Though writing tests may seem like extra work, they save time in the long run by reducing debugging time and ensuring stability.

## How to Write Unit Tests

### The Basics

#### Project structure

The test files should be located in the `tests` directory.
Then, for each source file/module, there should be a corresponding test file.
The tests directory should have the same directory structure as the source code.

For example, if we have the following project structure:

```text
src/
├── level_0/
│ ├── calculator.py
```

The test files should be located in the `tests` directory.

```text
tests/
├── level_0/
│ ├── test_calculator.py
```

The goal of unit testing is to verify that small, isolated units of code (usually functions or methods) perform correctly and handle edge cases as designed.

As such a unit test should be as simple as possible and test only one thing.

Take the following example of a calculator module:

```python title="calculator.py"
--8<-- "src/level_0/calculator.py"
```

We could test that module with a single test, like so:

```python title="test_calculator.py"
--8<-- "tests/level_0/test_calculator.py:too_complicated"
```

But that test is testing way too many different things. If it breaks, all we know is that the calculator doesn’t work any more, we don’t know which parts still work and which part broke.

Whereas if we split it into true unit tests, like so:

```python title="test_calculator.py"
--8<-- "tests/level_0/test_calculator.py:split"
```

If one test breaks, we instantly know which part of the calculator is broken. We even have a specific test for the edge case of the division operation.

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
