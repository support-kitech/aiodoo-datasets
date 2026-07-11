"""Metadata Builder for Evaluation Generator."""

from generators.evaluation.domain.metadata import EvaluationMetadata
from generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from generators.evaluation.factories.metadata_factory import MetadataFactory
from generators.evaluation.enums import (
    EvaluationType,
    BenchmarkCategory,
    DifficultyLevel,
)
from typing import Tuple


class MetadataBuilder:
    """Builds Metadata objects securely."""

    @staticmethod
    def build_evaluation_metadata(
        generator_version: str,
        protocol_version: str,
        schema_version: str,
        source_module: str,
        odoo_version: str,
        odoo_edition: str,
        evaluation_type: EvaluationType,
        difficulty: DifficultyLevel,
        complexity: int,
    ) -> EvaluationMetadata:
        """Build evaluation metadata."""
        return MetadataFactory.create_evaluation_metadata(
            generator_version=generator_version,
            protocol_version=protocol_version,
            schema_version=schema_version,
            source_module=source_module,
            odoo_version=odoo_version,
            odoo_edition=odoo_edition,
            evaluation_type=evaluation_type,
            difficulty=difficulty,
            complexity=complexity,
        )

    @staticmethod
    def build_benchmark_metadata(
        suite_version: str,
        benchmark_version: str,
        benchmark_name: str,
        benchmark_category: BenchmarkCategory,
        benchmark_description: str,
        target_generator: str,
        supported_odoo_versions: Tuple[str, ...],
        supported_protocols: Tuple[str, ...],
    ) -> BenchmarkMetadata:
        """Build benchmark metadata."""
        return MetadataFactory.create_benchmark_metadata(
            suite_version=suite_version,
            benchmark_version=benchmark_version,
            benchmark_name=benchmark_name,
            benchmark_category=benchmark_category,
            benchmark_description=benchmark_description,
            target_generator=target_generator,
            supported_odoo_versions=supported_odoo_versions,
            supported_protocols=supported_protocols,
        )
