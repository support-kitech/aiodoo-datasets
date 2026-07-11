"""Operation Analyzer implementation."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.results.operation_result import OperationResult


class OperationAnalyzer(BaseAnalyzer):
    """Extracts required CRUD actions targeting the discovered artifacts."""

    PRIORITY = 20

    def analyze(self, context: AnalysisContext) -> OperationResult:
        return OperationResult(is_successful=True, operations=())
