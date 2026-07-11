"""Base processor interfaces and context objects."""

import abc
from pathlib import Path
from dataclasses import dataclass, replace, field
from typing import Mapping
from types import MappingProxyType

from preprocessing.domain.stats import TransformationStatistics
from preprocessing.domain.file import Language


@dataclass(frozen=True, slots=True)
class ProcessorContext:
    """
    Immutable state passed sequentially between processors.
    Processors never mutate this object, but return a new instance using `dataclasses.replace`.
    """

    file_path: Path
    normalized_path: Path
    language: Language
    raw_content: str
    current_content: str
    metadata: Mapping[str, object] = field(default_factory=lambda: MappingProxyType({}))
    warnings: tuple[str, ...] = field(default_factory=tuple)
    statistics: TransformationStatistics = field(default_factory=TransformationStatistics)

    def with_update(self, **kwargs) -> "ProcessorContext":
        """Helper to create a new immutable context with updated fields."""
        if "metadata" in kwargs:
            kwargs["metadata"] = MappingProxyType(kwargs["metadata"])
        if "warnings" in kwargs:
            kwargs["warnings"] = tuple(kwargs["warnings"])
        if "normalized_path" in kwargs:
            kwargs["normalized_path"] = Path(kwargs["normalized_path"])
        return replace(self, **kwargs)


class BaseProcessor(abc.ABC):
    """
    Abstract base class for all Preprocessing Processors.
    Processors must be stateless and pure.
    """

    @property
    @abc.abstractmethod
    def priority(self) -> int:
        """
        Deterministic ordering priority. Lower numbers execute first.
        e.g., 10 for Whitespace, 20 for Syntax, 90 for Analysis.
        """
        pass

    @abc.abstractmethod
    def process(self, context: ProcessorContext) -> ProcessorContext:
        """
        Apply normalization logic to the context.
        Must return a new, immutable ProcessorContext.
        """
        pass
