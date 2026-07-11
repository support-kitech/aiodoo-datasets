"""Normalized File domain models for the Preprocessing Framework."""

from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from typing import Mapping
from types import MappingProxyType

from preprocessing.domain.stats import TransformationStatistics


class DuplicateStatus(Enum):
    """Classification for duplicate file detection."""
    
    UNIQUE = "UNIQUE"
    DUPLICATE = "DUPLICATE"
    REFERENCE = "REFERENCE"


class Language(Enum):
    """Supported file languages."""
    
    PYTHON = "PYTHON"
    XML = "XML"
    JSON = "JSON"
    CSV = "CSV"
    MARKDOWN = "MARKDOWN"
    TEXT = "TEXT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class NormalizedFile:
    """
    Immutable representation of a preprocessed file.
    No domain objects should mutate once instantiated.
    """
    
    file_path: Path
    normalized_path: Path
    language: "Language"
    raw_content: str
    normalized_content: str
    duplicate_status: DuplicateStatus
    metadata: Mapping[str, object] = MappingProxyType({})
    warnings: tuple[str, ...] = tuple()
    statistics: TransformationStatistics = TransformationStatistics()
