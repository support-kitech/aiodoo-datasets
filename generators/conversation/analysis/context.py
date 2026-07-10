"""Analysis context for Conversation Generator."""

from dataclasses import dataclass
from typing import Dict, Any
from types import MappingProxyType

@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """Immutable container for raw incoming protocol data."""
    input_protocols: MappingProxyType[str, Dict[str, Any]]
