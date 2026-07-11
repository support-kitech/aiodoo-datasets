"""Benchmark Suite Builder for Evaluation Generator."""

from typing import Tuple
from generators.evaluation.domain.benchmark_suite import BenchmarkSuite
from generators.evaluation.domain.evaluation_case import EvaluationCase
from generators.evaluation.enums import BenchmarkCategory
from generators.evaluation.factories.benchmark_suite_factory import (
    BenchmarkSuiteFactory,
)


class BenchmarkSuiteBuilder:
    """Orchestrates the construction of a BenchmarkSuite."""

    @staticmethod
    def build(
        catalog_id: str,
        suite_category: BenchmarkCategory,
        suite_name: str,
        cases: Tuple[EvaluationCase, ...],
    ) -> BenchmarkSuite:
        """Build a benchmark suite by orchestrating the factory."""
        return BenchmarkSuiteFactory.create(
            catalog_id=catalog_id, suite_category=suite_category, suite_name=suite_name, cases=cases
        )
