"""Benchmark Catalog domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.benchmark_suite import BenchmarkSuite

from aiodoo_datasets.generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata

@dataclass(frozen=True, slots=True)
class BenchmarkCatalog:
    """Immutable collection of benchmark suites."""
    catalog_id: str
    catalog_name: str
    metadata: BenchmarkMetadata
    suites: Tuple[BenchmarkSuite, ...]
