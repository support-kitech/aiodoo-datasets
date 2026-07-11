"""Pipeline Context for Evaluation Generator."""

from dataclasses import dataclass
from typing import Dict, Any
from types import MappingProxyType

@dataclass(frozen=True, slots=True)
class PipelineContext:
    """Immutable input configuration container for the evaluation pipeline."""
    source_protocols: MappingProxyType[str, Any]
    evaluation_type: str
    target_generator: str
    benchmark_name: str
    benchmark_category: str
    benchmark_description: str
    supported_odoo_versions: tuple[str, ...]
    supported_protocols: tuple[str, ...]
    generator_version: str
    protocol_version: str
    schema_version: str
