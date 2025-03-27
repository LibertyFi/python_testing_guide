# Welcome to the Python unit tests tutorial

## Prerequisites

- Python 3.11+
- pytest installed as a dev dependency
- pytest-asyncio installed as a dev dependency

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

#### When Mock is not enough

Sometimes using `Mock` is not enough. Let's take this new example class:

```python title="session.py"
--8<-- "src/level_3/session.py"
```

##### MagicMock

We can try testing the `connect` method with `Mock` as we did before:

```python title="test_session.py"
--8<-- "tests/level_3/test_session.py:missing_magic_method"
```

Unfortunately mocking the `active_connections` attribute with `Mock` doesn't work because `Mock` doesn't implement the magic/special `__add__` method so it can't effectively mock an `int`.

We could mock the `__add__` method ourselves, but that would be tedious and error-prone since it's not always obvious which magic methods are used by the code.

Fortunately, `Mock` has a subclass called `MagicMock` that automatically implements the magic/special methods:

```python title="test_session.py"
--8<-- "tests/level_3/test_session.py:magic_mock"
```

Using `MagicMock` we don't have to worry about mocking any magic/special methods ourselves.

!!! tip "Magic Methods"

    If you use the `spec` or `spec_set` arguments then only magic methods that exist in the spec will be created.
    You can override the magic methods of a `MagicMock` by setting them just like you would with a normal `Mock`.

##### AsyncMock

We'd also like to test the `aconnect` method, but it's an async function so we can't use a simple `Mock` to mock it.

Fortunately, `Mock` has a subclass called `AsyncMock` that can be used to mock async functions:

```python title="test_session.py"
--8<-- "tests/level_3/test_session.py:async_mock"
```

!!! tip "AsyncMock calls"

    You can use `assert_awaited_once()` or similar methods to check that an async function is awaited and not just called.

!!! warning "Decorator for async tests"

    The `@pytest.mark.asyncio` decorator is required on each async test.

#### Mocking a class

Sometimes we need to mock a class and not just an object or a function.

Let's take the following example:

```python title="session.py"
--8<-- "src/level_4/session.py"
```

Instead of passing the interface as an argument when creating the `Session` object, it is instantiated by the class itself at initialization.

So we need to mock the full class, not just an instance of it.

```python title="test_session.py"
--8<-- "tests/level_4/test_session.py:mock_class"
```

We use the `@patch` decorator to mock the `ServerInterface` class, then we create a `Mock` object and assign it to the `return_value` of the mock class.

!!! danger "Patch in the right place"

    When using the patch function, it's important to patch the function **where it's used**, not where it's defined.

    :white_check_mark: `patch("src.level_4.session.ServerInterface")`

    :x: ~~`patch("src.level_4.interface.ServerInterface")`~~

The test works fine, but we forgot to mock the `Database` class so the test is actually using the real Database, which could be dangerous!

So let's mock the `Database` class as well:

```python title="test_session.py"
--8<-- "tests/level_4/test_session.py:mock_db"
```

Since the `Database` class is used with a context manager, using `with`, through its `get` method, the mock definition is a bit more complicated.

!!! tip "Using `spec_set` or `spec` inside the patch decorator"

    Use `spec_set` or `spec` inside a patch decorator to specify the structure of the resulting mock.

!!! danger "The order of patch decorators matters"

    The patch decorators automatically provide the test function with the mocks as arguments. The arguments are provided in the same order as the decorators are applied to the function, which is the opposite order as the decorators appear above the test function. Thus the first argument will match the decorator closest to the function and the last argument the furthest.

    ```python
    @patch("xxx.b")
    @patch("xxx.a")
    def test_function(mock_a, mock_b):
        ...
    ```

### Test Fixtures

Let's use a new example class:

```python title="session.py"
--8<-- "src/level_5/session.py"
```

#### What are test fixtures?

In our example, any test of the `Session` class's `connect` method will need to mock the `ServerInterface` and `Database` classes as well as a `ConnectionCounter` object.
Duplicating the mock setup code would be a bad practice.

A test fixture allows us to create a test setup that is used by several tests.

It can create a mock and provide it to the tests:

```python title="test_session.py"
--8<-- "tests/level_5/test_session.py:fixture_mock"
```

It can also patch a class and provide the resulting mock to the tests:

```python title="test_session.py"
--8<-- "tests/level_5/test_session.py:fixture_patch"
```

!!! note "Patch decorator or context manager"

    As we've already seen, the `patch` function can be used as a decorator, which applies the patch to the scope of the test function.
    It can also be used as a context manager, in which case the patch is applied to the scope of the with block.

A test fixture can also return more complicated objects:

```python title="test_session.py"
--8<-- "tests/level_5/test_session.py:fixture_autouse"
```

#### How to use test fixtures

To use a test fixture, we just add it as an argument to the test function.

```python title="test_session.py"
--8<-- "tests/level_5/test_session.py:fixture_first_use"
```

The fixture code will be executed automatically before the test function is executed.

To use it in another test, we just pass it as an argument to that function as well and it will be executed again.

```python title="test_session.py"
--8<-- "tests/level_5/test_session.py:fixture_second_use"
```

We've successfully avoided duplicating the mock setup code.

But what about the `Database` class? We haven't added it as an argument to our test functions. So is the actual Database called by our tests?
No! The `mock_db_connection` fixture was declared with the `autouse` flag, which means that it will be used automatically by all tests, without needing to pass it as an argument to the test function.

!!! tip "Seeing logs when running the tests"

    By default when you run the tests using `pytest`, the logs from your code are not displayed.
    If you want to see them, you can run the tests with `-v --log-cli-level=INFO`.
    In our example, if you activate the logs, you'll see that the logs from the actual `Database` class only show up if the `autouse` flag is not set.

    ```python title="database.py"
    --8<-- "src/level_5/database.py:db_logs"
    ```

But what if we want to check that the code under test actually calls the database? Since the `mock_db_connection` fixture is automatically used by all tests, we don't have a reference to the mock on which to call `assert_called_once()` or similar methods.

Fortunately, we can pass the `mock_db_connection` fixture as an explicit argument to the test function and then reference it in the test.

```python title="test_session.py"
--8<-- "tests/level_5/test_session.py:fixture_explicit_use"
```

!!! danger "Combining fixtures and patch decorators"

    The patch decorators automatically provide the test function with the mocks as arguments. The arguments are provided in the same order as the decorators are applied to the function, which is the opposite order as the decorators appear above the test function. The arguments for the test fixtures must come after the arguments for the patch decorators:
    ```python
    @patch("xxx.b")
    @patch("xxx.a")
    def test_function(mock_a, mock_b, fixture_mock):
        ...
    ```

### Advanced Mocking

#### Side Effects

We've already seen that we can specify the return value of a mock.
But what if that's not enough?

Let's take the following example:

```python title="session.py"
--8<-- "src/level_6/session.py"
```

We want to test the `start` method. It uses the `connect` method and the `is_server_connected` method so if we want to implement a proper unit test, we need to mock both, otherwise we're actually testing all three methods at the same time.

First of all, we can define a fixture for the `ServerInterface` class:

```python title="test_session.py"
--8<-- "tests/level_6/test_session.py:mock_interface_class"
```

Second, we don't want our test to actually sleep for multiple seconds, we just want to check that it calls the `sleep` function, so let's define a fixture for the `time.sleep` function:

```python title="test_session.py"
--8<-- "tests/level_6/test_session.py:mock_sleep"
```

!!! danger "Patch in the right place"

    Remember: when using the patch function, it's important to patch the function **where it's used**, not where it's defined.

    :white_check_mark: `patch("src.level_6.session.time.sleep")`

    :x: ~~`patch("time.sleep")`~~

But there are two problems that we've not encountered yet:

- the behavior of the `start` method depends on what the `connect` method does, and not what it returns. How can we mock the behavior of a method and not just its return value?
- `is_server_connected` is called multiple times and the behavior of the `start` method depends on the value returned by this method each time it's called. How can we set multiple successive return values for a mock?

That's where the `side_effect` attribute comes in.

```python title="test_session.py"
--8<-- "tests/level_6/test_session.py:with_side_effect"
```

The `side_effect` attribute can serve multiple purposes:

- if set to a specific value, the mock will return that value every time its called, it's equivalent to setting the `return_value` attribute
- if set to an iterable, the mock will return successive values from the iterable each time its called
- if set to a function, the mock will call the function every time its called

Here we used the iterable and function cases.

If we don't specify the `side_effect`, the mock will not do anything, and that's a valid test case too!

```python title="test_session.py"
--8<-- "tests/level_6/test_session.py:without_side_effect"
```

!!! note "Mocking methods"

    It can be seen as overkill to mock the other methods of a given class when testing a single method even though each methods will have its own unit tests anyway. But by doing it this way, we're making sure that breaking one method will only break the tests of that specific method and not the tests of all methods which call it.

#### Checking Mock Calls

We've already seen that we can check if a mock has been called or not. But we can also check the details of the calls to the mock.

Let's take the following example:

```python title="session.py"
--8<-- "src/level_7/session.py"
```

We want to test the `send_messages` method.

Let's test what happens when the method is called with a single message:

```python title="test_session.py"
--8<-- "tests/level_7/test_session.py:one_call_with_argument"
```

We check that the mock was called with the correct argument using `assert_called_once_with`.

Let's add a test for a call with multiple messages:

```python title="test_session.py"
--8<-- "tests/level_7/test_session.py:multiple_calls_with_arguments"
```

We check the number of calls to the mock, as well as the order and content of the calls.

!!! tip "Order of mock calls"

    You can set the `any_order` flag of `assert_has_calls` to `True` if the order of the calls shouldn't matter.

#### Exceptions

There are two cases where we need to handle exceptions in our tests:

- the code is supposed to catch an exception
- the code is supposed to raise an exception

Let's take the following example:

```python title="session.py"
--8<-- "src/level_8/session.py"
```

As before, we start by defining a fixture for the `ServerInterface` class:

```python title="test_session.py"
--8<-- "tests/level_8/test_session.py:mock_interface_class"
```

##### Check that an exception is caught

Let's test that the `connect` method catches the `ConnectionError` exception raised by the `interface.connect_to_server` method:

```python title="test_session.py"
--8<-- "tests/level_8/test_session.py:caught_exception"
```

This is another purpose of the `side_effect` attribute: if provided with an exception class or instance, the mock will raise that exception instead of returning a value.

!!! tip "Clearing a side effect"

    A `side_effect` can be cleared by setting it to None

##### Check that an exception is raised

Let's test that the `connect` method raises the `SessionError` exception when expected:

```python title="test_session.py"
--8<-- "tests/level_8/test_session.py:raised_exception"
```

Since the code under test raises an exception, we need the test to catch it or it will crash. We also want to check that the exception was raised, that it's the correct exception type and that it's the correct message.
`pytest.raises` allows us to do all of this.

!!! tip "Match of pytest.raises"

    The match argument allows us to check that the exception message matches a specific regex pattern, not just a static string.
