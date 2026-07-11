"""Statistics tracker for the Approval Generator."""

from typing import Mapping, Any, Tuple
from types import MappingProxyType
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.rules.rule_set import RuleSet
from aiodoo_datasets.generators.approval.domain.evidence import Evidence


class ApprovalStatistics:
    """Calculates deterministic statistics for a generated Review."""

    @staticmethod
    def compile(
        review: Review, rule_set: RuleSet, evidence_pool: Tuple[Evidence, ...]
    ) -> Mapping[str, Any]:
        """Compile the aggregated statistics deterministically."""

        findings_count = len(review.findings)
        recommendations_count = len(review.recommendations)

        findings_by_severity = {}  # type: ignore[var-annotated]
        for finding in review.findings:
            severity = finding.severity.value
            findings_by_severity[severity] = findings_by_severity.get(severity, 0) + 1

        confidence_distribution = {review.decision.confidence.value: 1}

        return MappingProxyType(
            {
                "reviews_generated": 1,
                "approvals": 1 if review.decision.status.value == "APPROVED" else 0,
                "rejections": 1 if review.decision.status.value == "REJECTED" else 0,
                "changes_requested": 1
                if review.decision.status.value == "CHANGES_REQUESTED"
                else 0,
                "findings_total": findings_count,
                "findings_by_severity": findings_by_severity,
                "recommendations_total": recommendations_count,
                "rules_executed": len(rule_set.rules),
                "evidence_processed": len(evidence_pool),
                "average_findings": findings_count,  # For a single review, average is the total
                "average_recommendations": recommendations_count,
                "confidence_distribution": confidence_distribution,
            }
        )
