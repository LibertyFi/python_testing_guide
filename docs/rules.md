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

## Mocking

- As a unit test should test a single entity, mock everything that is not part of the entity under test, such as external functions, classes, etc.
- As a unit test should test a single entity, when testing a specific class method, mock the other methods of that same class as well.
- Use `MagicMock` and `AsyncMock`, avoid using `Mock` unless there’s a good reason not to auto mock the magic methods
- Use `MagicMock(spec_set=MyClass)` if only the class attributes need to be mocked
- Use `MagicMock(spec=MyClass)` if instance attributes need to be mocked
- Do not use `MagicMock` without `spec` or `spec_set`
- Beware that `name` can't be set as an attribute of a `MagicMock` using the one-liner syntax, it has to be set after the mock is created
- Use `@patch` decorators to mock things for a specific test
- Do not use the `patch` function as a context manager inside tests
- Use the `patch` function as a context manager inside test fixtures
- Use `patch.object` when patching an attribute of an object accessible in the test module, such as an imported class for example
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
