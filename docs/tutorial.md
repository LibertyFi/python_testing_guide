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

#### How big should each unit test be?

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

### Mocking

#### What is mocking?

Mocking is a technique used to replace a function or method with a mock implementation in order to test the code that uses it.

Take the following example of a simple class:

```python title="session.py"
--8<-- "src/level_1/session.py"
```

We could test the single method of the class like so:

```python title="test_session.py"
--8<-- "tests/level_1/test_session.py:no_mocking"
```

But the `connect_to_server` function comes from an external module, which we don't control in the `session` module.
Each unit test should only test one unit of code. This test is actually testing both `session.connect` and `interface.connect_to_server`.
If the test fails, there is no way to tell if it's because of the `connect` method or the `connect_to_server` function.

#### Mocking a function

To properly test the above `connect` method, we should mock the `connect_to_server` function. Here's how we can do it, using the `patch` function (here in decorator form):

```python title="test_session.py"
--8<-- "tests/level_1/test_session.py:with_mock"
```

Mocking the `connect_to_server` function has several benefits:

- we're only testing the `connect` method, regardless of the actual implementation of `connect_to_server`
- we're able to have two test cases for the `connect` method, one for when the connection is successful and one for when it's not because we control the return value of the mock
- we're not executing the actual `connect_to_server` function, which could require a specific setup, make network requests, or even be an expensive operation

!!! danger "Patch in the right place"

    When using the patch function, it's important to patch the function **where it's used**, not where it's defined.

    :white_check_mark: `patch("src.level_1.session.connect_to_server")`

    :x: ~~`patch("src.level_1.interface.connect_to_server")`~~

#### Mocking an object

Let's use the following class as an example:

```python title="session.py"
--8<-- "src/level_2/session.py"
```

In order to test the `connect` method, we first need to instantiate a `Session` object, which requires an `ServerInterface` object.

Since we don't know what creating an actual `ServerInterface` object entails, and we don't want to test the `ServerInterface` class, we need to mock the `ServerInterface` object.

##### Simple Mock

The simplest way to mock an object is to use the `Mock` class, from the `unittest.mock` module.

```python title="test_session.py"
--8<-- "tests/level_2/test_session.py:simple_mock"
```

Here we create a `Mock` object and assign a return value to its `connect_to_server` attribute.

Now when the test calls `session.connect()`, it will call the `connect_to_server` method of the `Mock` instead of an actual `ServerInterface` object.

And since we control the mock, we can even check that the `connect_to_server` method is indeed called by the `connect` method.

##### Specifying the Mock's Structure

`Mock` generates attributes on the fly so that the mock can be used automatically without worrying about setting it up.
The downside of this is that you can use attributes that don't even exist on the original object.

Here's an example:

```python title="interface.py"
--8<-- "src/level_2/interface.py"
```

```python title="test_session.py"
--8<-- "tests/level_2/test_session.py:mock_with_no_spec"
```

The `ServerInterface` object we want to mock doesn't have a `not_an_actual_attribute` attribute, so we shouldn't allow the mock to have it.
Moreover, even if the `connect` method actually uses `not_an_actual_attribute`, this test will still pass even though the attribute doesn't actually exist, which will make `connect` crash at runtime.

Thankfully, there are ways to specify the structure of the mock object.

The best (strictest) way is to use the `spec_set` argument to specify to the `Mock` constructor the class of the object we want to mock:

```python title="test_session.py"
--8<-- "tests/level_2/test_session.py:spec_set"
```

This will raise an error if we try to access an attribute that doesn't exist in the `ServerInterface` class.

Unfortunately, instance attributes are not part of the class specification, so they don't exist as far as `spec_set` is concerned.

```python title="test_session.py"
--8<-- "tests/level_2/test_session.py:spec_set_instance_attribute"
```

If you need to mock an instance attribute (or any attribute that is defined at runtime), you can use `spec` instead of `spec_set`:

```python title="test_session.py"
--8<-- "tests/level_2/test_session.py:simple_spec_for_instance_attribute"
```

!!! warning "`spec` vs `spec_set`"

    `spec` is not as strict as `spec_set`, it will simply ensure that an attribute can't be accessed if it has not been set, whether by the test or the specified class:

    ```python title="test_session.py"
    --8<-- "tests/level_2/test_session.py:spec_warning"
    ```

!!! tip "One-liner syntax"

    You can also define the mock and its attributes at the same time if you prefer the one-liner syntax.

    ```python title="test_session.py"
    --8<-- "tests/level_2/test_session.py:simple_spec_one_liner"
    ```

#### Mock vs MagicMock vs AsyncMock

#### Mocking a class

### Test Fixtures

### Advanced Mocking
