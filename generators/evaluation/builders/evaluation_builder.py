"""Evaluation Builder for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.evaluation import Evaluation
from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from aiodoo_datasets.generators.evaluation.factories.evaluation_factory import EvaluationFactory

class EvaluationBuilder:
    """Orchestrates the construction of the root Evaluation aggregate."""
    
    @staticmethod
    def build(
        generator_version: str,
        source_identifier: str,
        metadata: EvaluationMetadata,
        catalog: BenchmarkCatalog
    ) -> Evaluation:
        """Build an evaluation by orchestrating the factory."""
        return EvaluationFactory.create(
            generator_version=generator_version,
            source_identifier=source_identifier,
            metadata=metadata,
            catalog=catalog
        )
