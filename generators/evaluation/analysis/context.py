"""Analysis Context for Evaluation Generator."""

from dataclasses import dataclass
from typing import Any
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """Immutable context holding read-only input protocol structures."""

    source_protocols: MappingProxyType[str, Any]
    evaluation_type: str
