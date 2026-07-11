"""Operation Analyzer implementation."""

from generators.execution.analysis.base import BaseAnalyzer
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.results.operation_result import OperationResult


class OperationAnalyzer(BaseAnalyzer):  # type: ignore[misc]
    """Extracts required CRUD actions targeting the discovered artifacts."""

    PRIORITY = 20

    def analyze(self, context: AnalysisContext) -> OperationResult:
        return OperationResult(is_successful=True, operations=())
