"""Unit tests for the DecisionScorer."""

import unittest
from generators.approval.engine.scoring import DecisionScorer
from generators.approval.domain.finding import Finding
from generators.approval.enums import (
    RuleCategory,
    Severity,
    DecisionEnum,
    ConfidenceLevel,
)


class TestDecisionScorer(unittest.TestCase):
    def test_evaluate_decision_approved(self) -> None:
        findings = []
        decision, confidence, reasoning = DecisionScorer.evaluate_decision(findings)
        self.assertEqual(decision, DecisionEnum.APPROVED)
        self.assertEqual(confidence, ConfidenceLevel.MEDIUM)

    def test_evaluate_decision_rejected(self) -> None:
        finding = Finding(
            finding_id="f1",
            rule_id="SEC-001",
            category=RuleCategory.SECURITY,
            severity=Severity.CRITICAL,
            description="Critical security flaw",
            evidence=tuple(),
        )
        decision, confidence, reasoning = DecisionScorer.evaluate_decision([finding])
        self.assertEqual(decision, DecisionEnum.REJECTED)
        self.assertEqual(confidence, ConfidenceLevel.HIGH)

    def test_evaluate_decision_changes_requested(self) -> None:
        finding = Finding(
            finding_id="f2",
            rule_id="STYLE-001",
            category=RuleCategory.STYLE,
            severity=Severity.MEDIUM,
            description="Style violation",
            evidence=tuple(),
        )
        decision, confidence, reasoning = DecisionScorer.evaluate_decision([finding])
        self.assertEqual(decision, DecisionEnum.CHANGES_REQUESTED)
        self.assertEqual(confidence, ConfidenceLevel.HIGH)


if __name__ == "__main__":
    unittest.main()
