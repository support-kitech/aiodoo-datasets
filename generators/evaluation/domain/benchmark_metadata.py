"""Benchmark Metadata domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.evaluation.enums import BenchmarkCategory

@dataclass(frozen=True, slots=True)
class BenchmarkMetadata:
    """Immutable benchmark context data."""
    suite_version: str
    benchmark_version: str
    benchmark_name: str
    benchmark_category: BenchmarkCategory
    benchmark_description: str
    target_generator: str
    supported_odoo_versions: Tuple[str, ...]
    supported_protocols: Tuple[str, ...]
