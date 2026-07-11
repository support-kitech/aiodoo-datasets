"""Abstract base for all execution analyzers."""

from abc import ABC, abstractmethod
from typing import Any
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext


class BaseAnalyzer(ABC):
    """
    Abstract interface enforcing priority ordering and uniform analysis signatures.
    """

    PRIORITY: int

    @abstractmethod
    def analyze(self, context: AnalysisContext) -> Any:
        """Process the context and return a domain-specific Result object."""
        pass
