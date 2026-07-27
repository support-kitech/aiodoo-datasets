"""Pipeline Result for Evaluation Generator."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Optional, Tuple


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Immutable output container for the evaluation pipeline."""

    dataset: Tuple[Any, ...]
    statistics: MappingProxyType[str, Any]
    validation_passed: bool
    export_metadata: Optional[MappingProxyType[str, Any]] = None
    protocol_context: Any = None
    catalog: Any | None = None
