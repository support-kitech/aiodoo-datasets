from abc import ABC, abstractmethod
from typing import Any
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult


class BaseBuilder(ABC):
    """
    Abstract interface for all builders.
    Enforces PRIORITY, REQUIRES, INPUT, OUTPUT and the lifecycle hooks.
    """

    PRIORITY: int
    REQUIRES: tuple = ()  # type: ignore[type-arg]
    INPUT: Any
    OUTPUT: Any

    def before_build(self, context: BuilderContext) -> None:
        """Hook executed before build logic."""
        pass

    @abstractmethod
    def build(self, context: BuilderContext) -> BaseBuildResult:
        """Core stateless build logic mapping INPUT to OUTPUT."""
        pass

    def after_build(self, context: BuilderContext, result: BaseBuildResult) -> None:
        """Hook executed after build logic."""
        pass
