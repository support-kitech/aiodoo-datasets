"""Benchmark Catalog Factory for Evaluation Generator."""

import hashlib
from typing import Tuple
from generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from generators.evaluation.domain.benchmark_suite import BenchmarkSuite


class BenchmarkCatalogFactory:
    """Factory for creating immutable BenchmarkCatalog objects with deterministic IDs."""

    @staticmethod
    def generate_id(evaluation_id: str) -> str:
        """Generate a deterministic catalog ID."""
        hash_input = f"CTLG:{evaluation_id}"
        ctlg_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"CTLG-{ctlg_hash}"

    @staticmethod
    def create(
        evaluation_id: str,
        catalog_name: str,
        metadata: BenchmarkMetadata,
        suites: Tuple[BenchmarkSuite, ...],
    ) -> BenchmarkCatalog:
        """Create a new benchmark catalog with a hash-based deterministic ID."""
        catalog_id = BenchmarkCatalogFactory.generate_id(evaluation_id)

        return BenchmarkCatalog(
            catalog_id=catalog_id, catalog_name=catalog_name, metadata=metadata, suites=suites
        )
