"""Tests for the Protocol Mapper."""

import unittest
from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.finding import Finding
from aiodoo_datasets.generators.approval.domain.recommendation import Recommendation
from aiodoo_datasets.generators.approval.domain.decision import Decision
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.enums import DecisionEnum, ConfidenceLevel, Severity, RuleCategory
from aiodoo_datasets.generators.approval.protocol.mapper import ProtocolMapper

class TestProtocolMapper(unittest.TestCase):
    def test_map_review_to_protocol(self):
        evidence = Evidence(
            evidence_id="e1",
            source_generator=SourceGenerator.CODING,
            source_reference="node1",
            snippet="import os"
        )
        finding = Finding(
            finding_id="f1",
            rule_id="STYLE-001",
            category=RuleCategory.STYLE,
            severity=Severity.LOW,
            description="Style violation",
            evidence=(evidence,)
        )
        recommendation = Recommendation(
            recommendation_id="r1",
            finding_id="f1",
            description="Fix style",
            suggested_fix="import sys"
        )
        decision = Decision(
            decision_id="d1",
            status=DecisionEnum.CHANGES_REQUESTED,
            confidence=ConfidenceLevel.HIGH,
            reasoning="See findings."
        )
        metadata = ReviewMetadata(
            generator_version="1.0",
            protocol_version="1.0",
            schema_version="1.0",
            source_module="test_mod"
        )
        review = Review(
            review_id="rev1",
            metadata=metadata,
            decision=decision,
            findings=(finding,),
            recommendations=(recommendation,),
            evidence=(evidence,)
        )

        protocol = ProtocolMapper.map_review(review)

        self.assertEqual(protocol.review_id, "rev1")
        self.assertEqual(protocol.metadata.source_module, "test_mod")
        self.assertEqual(protocol.decision.status, "CHANGES_REQUESTED")
        self.assertEqual(len(protocol.findings), 1)
        self.assertEqual(protocol.findings[0].evidence[0].source_reference, "node1")
        self.assertEqual(len(protocol.recommendations), 1)

if __name__ == "__main__":
    unittest.main()
