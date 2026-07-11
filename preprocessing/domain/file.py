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

    def __getstate__(self):
        return (
            self.file_path,
            self.normalized_path,
            self.language,
            self.raw_content,
            self.normalized_content,
            self.duplicate_status,
            dict(self.metadata),
            self.warnings,
            self.statistics,
        )

    def __setstate__(self, state):
        (
            file_path,
            normalized_path,
            language,
            raw_content,
            normalized_content,
            duplicate_status,
            metadata_dict,
            warnings,
            statistics,
        ) = state
        object.__setattr__(self, "file_path", file_path)
        object.__setattr__(self, "normalized_path", normalized_path)
        object.__setattr__(self, "language", language)
        object.__setattr__(self, "raw_content", raw_content)
        object.__setattr__(self, "normalized_content", normalized_content)
        object.__setattr__(self, "duplicate_status", duplicate_status)
        object.__setattr__(self, "metadata", MappingProxyType(metadata_dict))
        object.__setattr__(self, "warnings", warnings)
        object.__setattr__(self, "statistics", statistics)
