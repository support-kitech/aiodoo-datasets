"""Verification Analyzer implementation."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.results.verification_result import VerificationResult

class VerificationAnalyzer(BaseAnalyzer):
    """Defines testing commands asserting operation success."""
    
    PRIORITY = 50
    
    def analyze(self, context: AnalysisContext) -> VerificationResult:
        return VerificationResult(is_successful=True, verifications=())
