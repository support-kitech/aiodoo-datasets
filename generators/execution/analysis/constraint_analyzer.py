"""Constraint Analyzer implementation."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.results.constraint_result import ConstraintResult

class ConstraintAnalyzer(BaseAnalyzer):
    """Discovers environmental constraints (e.g. Enterprise only) for operations."""
    
    PRIORITY = 40
    
    def analyze(self, context: AnalysisContext) -> ConstraintResult:
        return ConstraintResult(is_successful=True, constraints=())
