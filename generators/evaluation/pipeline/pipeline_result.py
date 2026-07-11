"""Pipeline Result for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple, Any, Optional
from types import MappingProxyType
# Protocol imports removed


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Immutable output container for the evaluation pipeline."""

    dataset: Tuple[Any, ...]
    statistics: MappingProxyType[str, Any]
    validation_passed: bool
    export_metadata: Optional[MappingProxyType[str, Any]] = None
    protocol_context: Any = None
