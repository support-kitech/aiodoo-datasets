"""Protocol mapper for the Approval Generator."""

from generators.approval.domain.review import Review
from generators.approval.protocol.domain.finding_protocol import (
    FindingProtocol,
    RecommendationProtocol,
    EvidenceProtocol,
)
from generators.approval.protocol.domain.decision_protocol import DecisionProtocol
from generators.approval.protocol.domain.approval_protocol import (
    ApprovalProtocol,
    ReviewMetadataProtocol,
)


class ProtocolMapper:
    """Maps internal domain models to external protocol models."""

    @staticmethod
    def map_review(review: Review) -> ApprovalProtocol:
        """Map a Review domain model to an ApprovalProtocol model."""
        return ApprovalProtocol(
            review_id=review.review_id,
            metadata=ReviewMetadataProtocol(
                generator_version=review.metadata.generator_version,
                protocol_version=review.metadata.protocol_version,
                schema_version=review.metadata.schema_version,
                source_module=review.metadata.source_module,
                odoo_version=review.metadata.odoo_version,
                odoo_edition=review.metadata.odoo_edition,
                planner_version=review.metadata.planner_version,
                coding_version=review.metadata.coding_version,
                execution_version=review.metadata.execution_version,
                repair_version=review.metadata.repair_version,
                complexity_score=review.metadata.complexity_score,
            ),
            decision=DecisionProtocol(
                decision_id=review.decision.decision_id,
                status=review.decision.status.value,
                confidence=review.decision.confidence.value,
                reasoning=review.decision.reasoning,
            ),
            findings=[
                FindingProtocol(
                    finding_id=f.finding_id,
                    rule_id=f.rule_id,
                    category=f.category.value,
                    severity=f.severity.value,
                    description=f.description,
                    is_positive=f.is_positive,
                    evidence=[
                        EvidenceProtocol(
                            evidence_id=e.evidence_id,
                            source_generator=e.source_generator.value,
                            source_reference=e.source_reference,
                            file_path=e.file_path,
                            line_number=e.line_number,
                            snippet=e.snippet,
                            description=e.description,
                        )
                        for e in f.evidence
                    ],
                )
                for f in review.findings
            ],
            recommendations=[
                RecommendationProtocol(
                    recommendation_id=r.recommendation_id,
                    finding_id=r.finding_id,
                    description=r.description,
                    suggested_fix=r.suggested_fix,
                )
                for r in review.recommendations
            ],
        )
