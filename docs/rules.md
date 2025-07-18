# Rules

Here are the rules to follow when writing tests:

## Project Structure

- Put all test files in the `tests` directory.
- The tests directory should have the same internal directory structure as the source code.

For example:

```text
project_root/
├── <src_dir>/
│ ├── feature_0/
│ │ ├── module_0.py
│ │ └── module_1.py
├── tests/
│ ├── feature_0/
│ │ ├── test_module_0.py
│ │ └── test_module_1.py
```

## What to test

The goal of unit testing is to verify that small, isolated units of code (usually functions or methods) perform correctly and handle edge cases as designed.

As such a unit test should be as simple as possible and test only one thing.

There should be enough tests to cover all the code paths and edge cases of the entity being tested. For instance there should be separate test cases for:

- branches of an `if` statement
- branches of a try/except block
- special values of arguments (None, empty objects, etc.)

The ultimate goal is to have a test coverage of 100% for the entity being tested, so that each part of the code will have been executed at least once when running the tests.

## Mocking

### What to mock

A unit test should test a single entity. So you should mock everything that is controlled by the entity being tested. For instance:

- All external functions, classes, etc. must be mocked. The only exceptions are standard libraries that don't require a specific setup to work, such as `datetime`, `math`, `random`, etc.
- When testing a specific method of a class, mock the other methods of that same class as well.

### How to mock

- Use `MagicMock` and `AsyncMock`, avoid using `Mock` unless there’s a good reason not to auto mock the magic methods
- Use `MagicMock(spec_set=MyClass)` if only the class attributes need to be mocked
- Use `MagicMock(spec=MyClass)` if instance attributes need to be mocked
- Do not use `MagicMock` without `spec` or `spec_set`
- Beware that `name` can't be set as an attribute of a `MagicMock` using the one-liner syntax, it has to be set after the mock is created
- Use `@patch` decorators to mock things for a specific test, do not use the `patch` function as a context manager inside the tests. There is only one exception to this rule: when you need to mock a module imported in the init method of an object, then you need to instanciate the object and then patch the imported module using the `patch` function as a context manager.
- When patching an attribute (not an imported module) of an instanciated object, simply use `object.attribute = MagicMock()/AsyncMock()`.
- However you can and should use the `patch` function as a context manager inside test fixtures
- Use `@patch.object` instead of `@patch` (and `patch.object` instead of `patch`) when patching an attribute or a method of an object accessible in the test module, such as a class that is imported by the test module. For instance, the correct way to mock the method of a class is `@patch.object(MyClass, "method")`.
- Keep in mind that the order of the decorators must match the **reverse** order of the arguments in the signature of the test function
- Use `spec` and `spec_set` in the patch if it patches a class or an object
- If the same patch or mock is used by more than 2 tests, define a test fixture

```python
@patch("xxx.b", spec_set=ClassToMock)
@patch("xxx.function")
def test_function(mock_function: MagicMock, mock_b: MagicMock, fixture_mock: MagicMock):
    ...
```

## File Structure

Structure your test file like so:

1. imports
2. common mock constants
3. test fixtures
4. tests

Use helper functions to avoid duplicating code between tests, for initialization code or mock setup for instance. Put the helper functions inbetween the tests, before the tests that use them.

Here's an example:

```python
import pytest

from src.feature_0.module_0 import MyClass

MOCK_CONSTANT = "mock_constant"

@pytest.fixture
def my_fixture():
    ...

def test_method_0(my_fixture):
    ...
    MyClass.method_0()
    ...

def helper_function():
    ...

def test_method_1(my_fixture):
    helper_function()
    ...
    MyClass.method_1()
    ...

def test_method_2(my_fixture):
    helper_function()
    ...
    MyClass.method_2()
    ...
```

## Test Structure

Structure your tests like so:

1. initialization of variables and mocks
2. call to the function under test
3. mock calls asserts
4. value asserts

Separate each part with an empty line.

The names of the test functions should follow this pattern:
`test_<name_of_the_tested_entity>_<description_of_the_test_case>`

Any test that uses async components must have the `@pytest.mark.asyncio` decorator, before any `patch` decorators.

Here's an example:

```python
@pytest.mark.asyncio
@patch("xxx.a")
async def test_method_0_xxx_is_false(mock_a: MagicMock, fixture_xxx_mock: MagicMock):
    mock_b = MagicMock()
    my_instance = MyClass(mock_a, mock_b)
    fixture_xxx_mock.return_value = False

    result = await my_instance.method_0()

    mock_a.method_0.assert_called_once()
    fixture_xxx_mock.assert_called_once()

    assert result == "expected_value"
```
