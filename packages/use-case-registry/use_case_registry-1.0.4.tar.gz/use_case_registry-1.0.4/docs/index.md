# What is this?

This library builds a set of core components I like to use when developing software. The documentation written here aims to be both a practice for me on how to write documentation of my projects and, most importantly, to give ideas on the logic and the reasons why I use this library when writting software.

## What does the library implement?

### `UseCaseRegistry` object

It's basically a fully typed `list` that is instantiated defining a max length. The use case of this object is to be injected into each use case defined workflow to collect a set of write operations that will be executed later as an ACID transaction against the application database.

**Note:** I do know that libraries like `SQLAlchemy` use *context managers* to implement the ***Unit Of Work*** pattern and that essentially everything that happens within the context will be executed as a transaction when triggering the `__exit__` magic method. But, after working with other type of databases that support ACID transactions (such as `DynamoDB`) I've found that this idea of a container that collects a set of operations is easier to generalize and to extend.

```python

from use_case_registry import UseCaseRegistry

MAX_SUPPORTED_WRITE_OPERATIONS = 100

write_ops_registry = UseCaseRegistry[str](max_length=10)
# UseCaseRegistry[int](max_length=3)
# UseCaseRegistry[Any](max_length=MAX_SUPPORTED_WRITE_OPERATIONS)

write_ops_registry.add_value(v="INSERT INTO...")
write_ops_registry.add_value(v="INSERT INTO...")
write_ops_registry.add_value(v="INSERT INTO...")

commit_as_transaction(write_operations=write_ops_registry.get_state())

```

### `ICommand` interface

The `Command` is a behavioral design pattern that turns a request into a stand-alone object that contains all information about the request (see [Refactoring Guru](https://refactoring.guru/design-patterns/command)). In this library the interface defines that all concrete implementations must implement a method called `validate`. 

This method either success, meaning all input arguments to the command class are valid (given the core logic context) or returns a `CommandInputValidationError` meaning at least one input argument is not valid.

```python
from result import Err, Ok, Result

from use_case_registry.base import ICommand
from use_case_registry.errors import CommandInputValidationError


class ConcreteCommand(ICommand):
    """A concrete command implementation."""

    def __init__(self, name: str, last_name: str, age: int) -> None:
        """ConcreteCommand constructor."""
        self.name = name
        self.last_name = last_name
        self.age = age

    def validate(self) -> Result[None, CommandInputValidationError]:
        """Validate command inputs are valid."""
        conditions = self.name.isascii() and self.last_name.isascii() and self.age > 0
        if not conditions:
            return Err(CommandInputValidationError())

        return Ok()

```

### `IUsecase` interface

Each use case is implemented as a workflow composed by a logic sequence of steps that are required to successfully complete the request (see [One Use Case, One Workflow](general-thoughts/one-use-case-one-workflow/index.md)).

The interface enforces to instantiate the concrete use case requiring a `write_ops_registry` in the constructor and the implementation of an `execute` method. Everything else is optional. I like to also required a concrete implementation of the `ICommand` interface. So you ensure all input arguments that all triggering your use case are valid in the context of your business logic.


```python
from result import Err, Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.base import ICommand, IUsecase
from use_case_registry.errors import CommandInputValidationError

MAX_SUPPORTED_WRITE_OPERATIONS = 100

write_ops_registry = UseCaseRegistry[str](max_length=10)


class GreetingCommand(ICommand):
    def __init__(self, name: str) -> None:
        self.name = name

    def validate(self) -> Result[None, CommandInputValidationError]:
        if not self.name.isascii():
            return Err(CommandInputValidationError())

        return Ok()


class ConcreteUseCase(IUsecase):
    def __init__(
        self, command: GreetingCommand, write_ops_registry: UseCaseRegistry[str]
    ) -> None:
        self.command = command
        self.database = IDatabase()
        super().__init__(write_ops_registry)

    def _compose_greeting(self) -> str:
        return f"Hi {self.command.name}"

    def execute(self) -> Result[str, Exception]:
        composed_greeting = self._compose_greeting()

        # This is deterministic. We are adding a string to the `UseCaseRegistry`
        self.database.increase_number_of_greeting_done(
            write_ops_registry=self.write_ops_registry
        )

        # This is not deterministic so an error handling has to be implemented.
        success_or_err = self.database.commit_transacation(
            write_ops_registry=self.write_ops_registry
        )
        err = success_or_err.err()
        if err is not None:
            # handle error
            return Err(RuntimeError())
        
        return Ok(composed_greeting)
```