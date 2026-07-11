"""Analysis Layer for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.analysis.context import AnalysisContext
from aiodoo_datasets.generators.evaluation.analysis.result import AnalysisResult
from aiodoo_datasets.generators.evaluation.analysis.evidence_extractor import EvidenceExtractor
from aiodoo_datasets.generators.evaluation.analysis.ground_truth_extractor import GroundTruthExtractor
from aiodoo_datasets.generators.evaluation.analysis.difficulty_estimator import DifficultyEstimator
from aiodoo_datasets.generators.evaluation.analysis.complexity_estimator import ComplexityEstimator

# Ensure parsers are imported to trigger registry registration
from aiodoo_datasets.generators.evaluation.analysis import parsers

__all__ = [
    "AnalysisContext",
    "AnalysisResult",
    "EvidenceExtractor",
    "GroundTruthExtractor",
    "DifficultyEstimator",
    "ComplexityEstimator",
    "parsers",
]
