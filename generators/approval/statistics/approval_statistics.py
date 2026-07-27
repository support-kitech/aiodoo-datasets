"""Statistics tracker for the Approval Generator."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping, Sequence

from generators.approval.domain.evidence import Evidence
from generators.approval.domain.review import Review
from generators.approval.policy import MAX_EVIDENCE_ITEMS
from generators.approval.rules.rule_set import RuleSet


class ApprovalStatistics:
    """Calculates deterministic statistics for generated Approval reviews."""

    @staticmethod
    def compile(
        review: Review, rule_set: RuleSet, evidence_pool: tuple[Evidence, ...]
    ) -> Mapping[str, Any]:
        """Compile statistics for a single review (compat wrapper)."""
        return ApprovalStatistics.compile_many((review,), rule_set, evidence_pool=evidence_pool)

    @staticmethod
    def compile_many(
        reviews: Sequence[Review],
        rule_set: RuleSet,
        *,
        evidence_pool: tuple[Evidence, ...] | None = None,
    ) -> Mapping[str, Any]:
        """Compile aggregated statistics across all subject decisions."""
        approvals = 0
        rejections = 0
        changes_requested = 0
        findings_total = 0
        recommendations_total = 0
        evidence_written = 0
        findings_by_severity: dict[str, int] = {}
        confidence_distribution: dict[str, int] = {}
        by_capability: dict[str, int] = {}

        for review in reviews:
            status = review.decision.status.value
            if status == "APPROVED":
                approvals += 1
            elif status == "REJECTED":
                rejections += 1
            elif status == "CHANGES_REQUESTED":
                changes_requested += 1

            findings_total += len(review.findings)
            recommendations_total += len(review.recommendations)
            evidence_written += len(review.evidence)

            for finding in review.findings:
                severity = finding.severity.value
                findings_by_severity[severity] = findings_by_severity.get(severity, 0) + 1

            conf = review.decision.confidence.value
            confidence_distribution[conf] = confidence_distribution.get(conf, 0) + 1

            cap = review.capability or "unknown"
            by_capability[cap] = by_capability.get(cap, 0) + 1

        count = len(reviews)
        evidence_processed = len(evidence_pool) if evidence_pool is not None else evidence_written

        return MappingProxyType(
            {
                "reviews_generated": count,
                "approvals": approvals,
                "rejections": rejections,
                "changes_requested": changes_requested,
                "findings_total": findings_total,
                "findings_by_severity": findings_by_severity,
                "recommendations_total": recommendations_total,
                "rules_executed": len(rule_set.rules),
                "evidence_processed": evidence_processed,
                "evidence_written": evidence_written,
                "max_evidence_items": MAX_EVIDENCE_ITEMS,
                "average_findings": (findings_total / count) if count else 0.0,
                "average_recommendations": (recommendations_total / count) if count else 0.0,
                "confidence_distribution": confidence_distribution,
                "by_capability": by_capability,
            }
        )
