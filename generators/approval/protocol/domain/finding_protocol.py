"""Finding protocol model."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass(frozen=True, slots=True)
class EvidenceProtocol:
    """Serializable evidence structure."""
    evidence_id: str
    source_generator: str
    source_reference: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    snippet: Optional[str] = None
    description: str = ""

@dataclass(frozen=True, slots=True)
class RecommendationProtocol:
    """Serializable recommendation structure."""
    recommendation_id: str
    finding_id: str
    description: str
    suggested_fix: Optional[str] = None

@dataclass(frozen=True, slots=True)
class FindingProtocol:
    """Serializable finding structure."""
    finding_id: str
    rule_id: str
    category: str
    severity: str
    description: str
    evidence: List[EvidenceProtocol] = field(default_factory=list)
    is_positive: bool = False
