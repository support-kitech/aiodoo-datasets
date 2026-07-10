"""Unit tests for the Approval Generator domain models."""

import unittest
from dataclasses import FrozenInstanceError
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata
from aiodoo_datasets.generators.approval.domain.finding import Finding
from aiodoo_datasets.generators.approval.domain.decision import Decision
from aiodoo_datasets.generators.approval.domain.recommendation import Recommendation
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.enums import DecisionEnum, ConfidenceLevel, Severity, RuleCategory

class TestDomainModels(unittest.TestCase):
    """Test immutability and initialization of domain models."""

    def test_evidence_immutability(self):
        from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
        evidence = Evidence(evidence_id="e1", source_generator=SourceGenerator.CODING, source_reference="node1")
        with self.assertRaises(FrozenInstanceError):
            evidence.description = "new description"

    def test_finding_immutability(self):
        from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
        evidence = Evidence(evidence_id="e1", source_generator=SourceGenerator.CODING, source_reference="node1")
        finding = Finding(
            finding_id="f1",
            rule_id="r1",
            category=RuleCategory.ARCHITECTURE,
            severity=Severity.HIGH,
            description="Test finding",
            evidence=(evidence,)
        )
        with self.assertRaises(FrozenInstanceError):
            finding.description = "new description"
        
        self.assertEqual(finding.evidence[0].evidence_id, "e1")

    def test_decision_immutability(self):
        decision = Decision(decision_id="d1", status=DecisionEnum.APPROVED, confidence=ConfidenceLevel.HIGH, reasoning="Looks good.")
        with self.assertRaises(FrozenInstanceError):
            decision.reasoning = "Bad"

    def test_metadata_immutability(self):
        metadata = ReviewMetadata(generator_version="1.0", protocol_version="1.0", schema_version="1.0", source_module="test_mod")
        with self.assertRaises(FrozenInstanceError):
            metadata.complexity_score = 10

    def test_review_immutability(self):
        metadata = ReviewMetadata(generator_version="1.0", protocol_version="1.0", schema_version="1.0", source_module="test_mod")
        decision = Decision(decision_id="d1", status=DecisionEnum.APPROVED, confidence=ConfidenceLevel.HIGH, reasoning="Looks good.")
        review = Review(review_id="rev1", metadata=metadata, decision=decision)
        with self.assertRaises(FrozenInstanceError):
            review.review_id = "rev2"

if __name__ == "__main__":
    unittest.main()
