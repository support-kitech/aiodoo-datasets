"""Analysis Result for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple, Any
from types import MappingProxyType

@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Immutable extracted analysis result consumed by Builders."""
    extracted_evidence: Tuple[MappingProxyType[str, Any], ...]
    ground_truth_structures: Tuple[MappingProxyType[str, Any], ...]
    estimated_difficulty: str
    estimated_complexity: int
