"""Benchmark Suite domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.evaluation_case import EvaluationCase

@dataclass(frozen=True, slots=True)
class BenchmarkSuite:
    """Immutable benchmark suite logically grouping evaluation cases."""
    suite_id: str
    suite_name: str
    cases: Tuple[EvaluationCase, ...]
