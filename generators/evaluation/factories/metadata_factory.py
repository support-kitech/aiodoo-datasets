"""Metadata Factory for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from aiodoo_datasets.generators.evaluation.enums import EvaluationType, BenchmarkCategory, DifficultyLevel
from typing import Tuple

class MetadataFactory:
    """Factory for creating immutable Metadata objects."""
    
    @staticmethod
    def create_evaluation_metadata(
        generator_version: str,
        protocol_version: str,
        schema_version: str,
        source_module: str,
        odoo_version: str,
        odoo_edition: str,
        evaluation_type: EvaluationType,
        difficulty: DifficultyLevel,
        complexity: int
    ) -> EvaluationMetadata:
        """Create evaluation metadata."""
        return EvaluationMetadata(
            generator_version=generator_version,
            protocol_version=protocol_version,
            schema_version=schema_version,
            source_module=source_module,
            odoo_version=odoo_version,
            odoo_edition=odoo_edition,
            evaluation_type=evaluation_type,
            difficulty=difficulty,
            complexity=complexity
        )
        
    @staticmethod
    def create_benchmark_metadata(
        suite_version: str,
        benchmark_version: str,
        benchmark_name: str,
        benchmark_category: BenchmarkCategory,
        benchmark_description: str,
        target_generator: str,
        supported_odoo_versions: Tuple[str, ...],
        supported_protocols: Tuple[str, ...]
    ) -> BenchmarkMetadata:
        """Create benchmark metadata."""
        return BenchmarkMetadata(
            suite_version=suite_version,
            benchmark_version=benchmark_version,
            benchmark_name=benchmark_name,
            benchmark_category=benchmark_category,
            benchmark_description=benchmark_description,
            target_generator=target_generator,
            supported_odoo_versions=supported_odoo_versions,
            supported_protocols=supported_protocols
        )
