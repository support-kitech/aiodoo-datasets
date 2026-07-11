"""Tests for the Rule System."""

import unittest
from generators.approval.rules.security_rules import SQLInjectionRule
from generators.approval.rules.style_rules import Pep8ComplianceRule
from generators.approval.rules.rule_context import RuleContext
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.source_generator import SourceGenerator
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.enums import Severity


class TestRuleSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata = ReviewMetadata(
            generator_version="1.0",
            protocol_version="1.0",
            source_module="test",
            schema_version="1.0",
            odoo_version="18.0",
            odoo_edition="CE",
        )

    def test_sql_injection_rule(self) -> None:
        rule = SQLInjectionRule()

        # Test positive match (vulnerable code)
        evidence_vuln = Evidence(
            evidence_id="e1",
            source_generator=SourceGenerator.CODING,
            source_reference="node1",
            snippet='cursor.execute(f"SELECT * FROM users WHERE id={user_id}")',
        )
        context = RuleContext(evidence_pool=(evidence_vuln,), metadata=self.metadata)
        result = rule.evaluate(context)
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].severity, Severity.CRITICAL)

        # Test negative match (safe code)
        evidence_safe = Evidence(
            evidence_id="e2",
            source_generator=SourceGenerator.CODING,
            source_reference="node2",
            snippet='cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))',
        )
        context_safe = RuleContext(evidence_pool=(evidence_safe,), metadata=self.metadata)
        result_safe = rule.evaluate(context_safe)
        self.assertEqual(len(result_safe.findings), 0)

    def test_pep8_compliance_rule(self) -> None:
        rule = Pep8ComplianceRule()

        evidence_bad = Evidence(
            evidence_id="e3",
            source_generator=SourceGenerator.CODING,
            source_reference="node3",
            snippet="from odoo import *\nclass MyModel(models.Model):\n    pass",
        )
        context = RuleContext(evidence_pool=(evidence_bad,), metadata=self.metadata)
        result = rule.evaluate(context)
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].severity, Severity.LOW)


if __name__ == "__main__":
    unittest.main()
