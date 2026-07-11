"""Analysis context for the Approval Generator."""

from dataclasses import dataclass
from typing import Mapping, Any


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """Immutable state holding the ingested protocols for review."""

    input_protocols: Mapping[str, Mapping[str, Any]]
