"""Metadata domain model for Evaluation Generator."""

from dataclasses import dataclass
from aiodoo_datasets.generators.evaluation.enums import EvaluationType, DifficultyLevel


@dataclass(frozen=True, slots=True)
class EvaluationMetadata:
    """Immutable evaluation context data."""

    generator_version: str
    protocol_version: str
    schema_version: str
    source_module: str
    odoo_version: str
    odoo_edition: str
    evaluation_type: EvaluationType
    difficulty: DifficultyLevel
    complexity: int
