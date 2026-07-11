"""Evaluation Aggregate domain model for Evaluation Generator."""

from dataclasses import dataclass
from generators.evaluation.domain.metadata import EvaluationMetadata
from generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog


@dataclass(frozen=True, slots=True)
class Evaluation:
    """Immutable root aggregate for the entire evaluation dataset generation."""

    evaluation_id: str
    metadata: EvaluationMetadata
    catalog: BenchmarkCatalog
