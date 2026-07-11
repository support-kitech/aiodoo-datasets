"""Unit tests for ApprovalStatistics."""

import unittest
from aiodoo_datasets.generators.approval.statistics.approval_statistics import ApprovalStatistics
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.domain.decision import Decision
from aiodoo_datasets.generators.approval.domain.finding import Finding
from aiodoo_datasets.generators.approval.enums import (
    DecisionEnum,
    ConfidenceLevel,
    RuleCategory,
    Severity,
)
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata
from aiodoo_datasets.generators.approval.rules.rule_set import RuleSet


class TestApprovalStatistics(unittest.TestCase):
    def test_compile_statistics(self) -> None:
        metadata = ReviewMetadata(
            generator_version="1.0.0",
            protocol_version="1.0",
            schema_version="1.0",
            source_module="test.module",
            odoo_version="18.0",
            odoo_edition="enterprise",
            complexity_score=10,
        )

        decision = Decision(
            decision_id="DEC-123",
            status=DecisionEnum.CHANGES_REQUESTED,
            confidence=ConfidenceLevel.HIGH,
            reasoning="Fix issues",
        )

        finding = Finding(
            finding_id="FND-123",
            rule_id="R-001",
            category=RuleCategory.SECURITY,
            severity=Severity.HIGH,
            description="Bad code",
            evidence=tuple(),
        )

        review = Review(
            review_id="REV-123",
            metadata=metadata,
            decision=decision,
            findings=(finding,),
            recommendations=tuple(),
            evidence=tuple(),
        )

        rule_set = RuleSet(rules=tuple())
        evidence_pool = tuple()

        stats = ApprovalStatistics.compile(review, rule_set, evidence_pool)

        self.assertEqual(stats["reviews_generated"], 1)
        self.assertEqual(stats["approvals"], 0)
        self.assertEqual(stats["changes_requested"], 1)
        self.assertEqual(stats["findings_total"], 1)
        self.assertEqual(stats["findings_by_severity"]["HIGH"], 1)
        self.assertEqual(stats["confidence_distribution"]["HIGH"], 1)
