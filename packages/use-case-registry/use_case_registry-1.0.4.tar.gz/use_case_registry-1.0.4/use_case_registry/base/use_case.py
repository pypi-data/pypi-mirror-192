"""Interface for concrete usecases."""
import abc
from typing import Any

from result import Result

from use_case_registry.registry import UseCaseRegistry


class IUsecase(abc.ABC):
    """Use case interface."""

    def __init__(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> None:
        """use case constructor."""
        self.write_ops_registry = write_ops_registry

    @abc.abstractmethod
    def execute(
        self,
    ) -> Result[Any, Exception]:
        """Workflow execution command to complete the use case."""
