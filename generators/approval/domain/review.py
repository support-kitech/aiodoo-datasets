"""Review domain model — one Review = one Approval training unit (one subject)."""

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from generators.approval.domain.decision import Decision
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.finding import Finding
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.domain.recommendation import Recommendation


@dataclass(frozen=True, slots=True)
class Review:
    """One subject decision with bounded evidence (ApprovalRequest/Response grain)."""

    review_id: str
    metadata: ReviewMetadata
    decision: Decision
    findings: Tuple[Finding, ...] = field(default_factory=tuple)
    recommendations: Tuple[Recommendation, ...] = field(default_factory=tuple)
    evidence: Tuple[Evidence, ...] = field(default_factory=tuple)
    record_id: str = ""
    capability: str = ""
    subject_id: str = ""
    source_object_id: str = ""
    subject: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
