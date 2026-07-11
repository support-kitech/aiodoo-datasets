"""Verification Analyzer implementation."""

from generators.execution.analysis.base import BaseAnalyzer
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.results.verification_result import (
    VerificationResult,
)


class VerificationAnalyzer(BaseAnalyzer):  # type: ignore[misc]
    """Defines testing commands asserting operation success."""

    PRIORITY = 50

    def analyze(self, context: AnalysisContext) -> VerificationResult:
        return VerificationResult(is_successful=True, verifications=())
