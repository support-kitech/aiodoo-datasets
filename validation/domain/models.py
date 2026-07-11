"""Immutable domain models for the Validation Framework."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping
from types import MappingProxyType

from validation.domain.enums import ValidationSeverity, ValidationCategory


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single validation finding. Immutable and deterministic."""

    rule_id: str
    severity: ValidationSeverity
    category: ValidationCategory
    message: str
    dataset_name: str
    record_index: int | None = None
    field_path: str = ""
    context: Mapping[str, object] = field(default_factory=lambda: MappingProxyType({}))


@dataclass(frozen=True, slots=True)
class ValidationContext:
    """Immutable snapshot of all artifacts to validate."""

    dataset_dir: Path
    dataset_files: tuple[Path, ...] = ()
    manifest_files: tuple[Path, ...] = ()
    statistics_files: tuple[Path, ...] = ()
    protocol_context: object | None = None
    metadata: Mapping[str, object] = field(default_factory=lambda: MappingProxyType({}))
