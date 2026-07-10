"""Analyzer for the Approval Generator."""

from typing import Tuple
from aiodoo_datasets.generators.approval.analysis.context import AnalysisContext
from aiodoo_datasets.generators.approval.analysis.result import AnalysisResult
from aiodoo_datasets.generators.approval.analysis.evidence_collector import EvidenceCollector
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata

class ApprovalAnalyzer:
    """Ingests protocol outputs and orchestrates evidence collection."""
    
    @staticmethod
    def analyze(context: AnalysisContext) -> AnalysisResult:
        """Analyze the input protocols to produce the evidence pool."""
        
        # Initialize evidence list
        evidence_list = []
        
        if context.input_protocols:
            evidence_list = EvidenceCollector.collect(context.input_protocols)
            
        return AnalysisResult(
            success=True,
            metadata=None,  # Handled upstream
            evidence_pool=tuple(evidence_list),
            diagnostics=tuple(),
        )
