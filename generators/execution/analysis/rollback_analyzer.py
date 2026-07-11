"""Rollback Analyzer implementation."""

from generators.execution.analysis.base import BaseAnalyzer
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.results.rollback_result import RollbackResult


class RollbackAnalyzer(BaseAnalyzer):  # type: ignore[misc]
    """Defines reversion commands if operation failure occurs."""

    PRIORITY = 60

    def analyze(self, context: AnalysisContext) -> RollbackResult:
        return RollbackResult(is_successful=True, rollbacks=())
