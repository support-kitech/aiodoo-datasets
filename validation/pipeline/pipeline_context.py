"""Immutable pipeline context for the Validation Framework."""

from dataclasses import dataclass

from validation.domain.models import ValidationContext
from validation.pipeline.pipeline_options import ValidationOptions
from validation.rules.registry import RuleRegistry
from validation.schemas.registry import SchemaRegistry


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """Immutable context object passed through the validation pipeline."""

    validation_context: ValidationContext
    options: ValidationOptions
    registry: RuleRegistry
    schema_registry: SchemaRegistry
