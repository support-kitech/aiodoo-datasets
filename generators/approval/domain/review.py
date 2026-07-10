"""Review domain model."""

from dataclasses import dataclass, field
from typing import Tuple
from aiodoo_datasets.generators.approval.domain.finding import Finding
from aiodoo_datasets.generators.approval.domain.recommendation import Recommendation
from aiodoo_datasets.generators.approval.domain.decision import Decision
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata

@dataclass(frozen=True, slots=True)
class Review:
    """The aggregate root containing all review components."""
    review_id: str
    metadata: ReviewMetadata
    decision: Decision
    findings: Tuple[Finding, ...] = field(default_factory=tuple)
    recommendations: Tuple[Recommendation, ...] = field(default_factory=tuple)
    evidence: Tuple[Evidence, ...] = field(default_factory=tuple)
