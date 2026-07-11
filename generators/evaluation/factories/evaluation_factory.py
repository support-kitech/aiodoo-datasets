"""Evaluation Factory for Evaluation Generator."""

import hashlib
from aiodoo_datasets.generators.evaluation.domain.evaluation import Evaluation
from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog


class EvaluationFactory:
    """Factory for creating immutable Evaluation objects with deterministic IDs."""

    @staticmethod
    def generate_id(generator_version: str, source_identifier: str) -> str:
        """Generate a deterministic root evaluation ID."""
        hash_input = f"EVALROOT:{generator_version}:{source_identifier}"
        eval_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"EVALROOT-{eval_hash}"

    @staticmethod
    def create(
        generator_version: str,
        source_identifier: str,
        metadata: EvaluationMetadata,
        catalog: BenchmarkCatalog,
    ) -> Evaluation:
        """Create a new root evaluation with a hash-based deterministic ID."""
        evaluation_id = EvaluationFactory.generate_id(generator_version, source_identifier)

        return Evaluation(evaluation_id=evaluation_id, metadata=metadata, catalog=catalog)
