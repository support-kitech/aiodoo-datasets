"""Constraint Analyzer implementation."""

from generators.execution.analysis.base import BaseAnalyzer
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.results.constraint_result import ConstraintResult


class ConstraintAnalyzer(BaseAnalyzer):  # type: ignore[misc]
    """Discovers environmental constraints (e.g. Enterprise only) for operations."""

    PRIORITY = 40

    def analyze(self, context: AnalysisContext) -> ConstraintResult:
        return ConstraintResult(is_successful=True, constraints=())
