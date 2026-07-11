"""Benchmark Catalog Builder for Evaluation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from aiodoo_datasets.generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from aiodoo_datasets.generators.evaluation.domain.benchmark_suite import BenchmarkSuite
from aiodoo_datasets.generators.evaluation.factories.benchmark_catalog_factory import BenchmarkCatalogFactory

class BenchmarkCatalogBuilder:
    """Orchestrates the construction of a BenchmarkCatalog."""
    
    @staticmethod
    def build(
        evaluation_id: str,
        catalog_name: str,
        metadata: BenchmarkMetadata,
        suites: Tuple[BenchmarkSuite, ...]
    ) -> BenchmarkCatalog:
        """Build a benchmark catalog by orchestrating the factory."""
        return BenchmarkCatalogFactory.create(
            evaluation_id=evaluation_id,
            catalog_name=catalog_name,
            metadata=metadata,
            suites=suites
        )
