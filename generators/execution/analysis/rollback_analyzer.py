"""Rollback Analyzer implementation."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.results.rollback_result import RollbackResult


class RollbackAnalyzer(BaseAnalyzer):
    """Defines reversion commands if operation failure occurs."""

    PRIORITY = 60

    def analyze(self, context: AnalysisContext) -> RollbackResult:
        return RollbackResult(is_successful=True, rollbacks=())
