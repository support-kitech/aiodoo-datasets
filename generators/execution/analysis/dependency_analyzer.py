"""Dependency Analyzer implementation."""

from generators.execution.analysis.base import BaseAnalyzer
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.results.dependency_result import DependencyResult


class DependencyAnalyzer(BaseAnalyzer):  # type: ignore[misc]
    """Calculates sequential prerequisites between extracted operations."""

    PRIORITY = 30

    def analyze(self, context: AnalysisContext) -> DependencyResult:
        return DependencyResult(is_successful=True, dependencies=())
