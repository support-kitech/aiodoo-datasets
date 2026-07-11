"""Approval protocol model."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from aiodoo_datasets.generators.approval.protocol.domain.finding_protocol import (
    FindingProtocol,
    RecommendationProtocol,
)
from aiodoo_datasets.generators.approval.protocol.domain.decision_protocol import DecisionProtocol


@dataclass(frozen=True, slots=True)
class ReviewMetadataProtocol:
    """Serializable metadata structure."""

    generator_version: str
    protocol_version: str
    schema_version: str
    source_module: str
    odoo_version: Optional[str] = None
    odoo_edition: Optional[str] = None
    planner_version: Optional[str] = None
    coding_version: Optional[str] = None
    execution_version: Optional[str] = None
    repair_version: Optional[str] = None
    complexity_score: Optional[int] = None


@dataclass(frozen=True, slots=True)
class ApprovalProtocol:
    """Root serializable approval review structure."""

    review_id: str
    metadata: ReviewMetadataProtocol
    decision: DecisionProtocol
    findings: List[FindingProtocol] = field(default_factory=list)
    recommendations: List[RecommendationProtocol] = field(default_factory=list)

    def model_dump(self) -> Dict[str, Any]:
        """Serialize the dataclass to a dictionary for DatasetWriter."""
        import dataclasses

        return dataclasses.asdict(self)
