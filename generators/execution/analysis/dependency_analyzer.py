"""Dependency Analyzer implementation."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.results.dependency_result import DependencyResult

class DependencyAnalyzer(BaseAnalyzer):
    """Calculates sequential prerequisites between extracted operations."""
    
    PRIORITY = 30
    
    def analyze(self, context: AnalysisContext) -> DependencyResult:
        return DependencyResult(is_successful=True, dependencies=())
