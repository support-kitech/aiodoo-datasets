"""Recommendation builder for the Approval Generator."""

from typing import Tuple
from generators.approval.domain.finding import Finding
from generators.approval.domain.recommendation import Recommendation


class RecommendationBuilder:
    """Builds recommendations based on review findings."""

    @staticmethod
    def build(findings: Tuple[Finding, ...]) -> Tuple[Recommendation, ...]:
        """Generate deterministic recommendations for negative findings."""
        recommendations = []
        for finding in findings:
            if not finding.is_positive:
                recommendations.append(
                    Recommendation(
                        recommendation_id=f"REC-{finding.finding_id}",
                        finding_id=finding.finding_id,
                        description=f"Address finding: {finding.description}",
                        suggested_fix="Review architecture and apply standard patterns.",
                    )
                )
        return tuple(recommendations)
