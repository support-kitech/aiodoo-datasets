"""Style rules for the Approval Generator."""

import hashlib
from types import MappingProxyType
from aiodoo_datasets.generators.approval.rules.base_rule import BaseRule
from aiodoo_datasets.generators.approval.rules.rule_context import RuleContext
from aiodoo_datasets.generators.approval.rules.rule_result import RuleResult
from aiodoo_datasets.generators.approval.enums import RuleCategory, Severity
from aiodoo_datasets.generators.approval.domain.finding import Finding


class Pep8ComplianceRule(BaseRule):  # type: ignore[misc]
    """Detects basic PEP-8 violations."""

    RULE_ID = "STYLE-001"
    RULE_NAME = "PEP-8 Compliance"
    RULE_CATEGORY = RuleCategory.STYLE
    SEVERITY = Severity.LOW
    DESCRIPTION = "Star imports are strongly discouraged by PEP-8."
    VERSION = "1.0"
    PRIORITY = 200

    def evaluate(self, context: RuleContext) -> RuleResult:
        findings = []

        for evidence in context.evidence_pool:
            if evidence.source_generator.value == "CODING" and evidence.snippet:
                if "import *" in evidence.snippet:
                    hash_input = f"{self.RULE_ID}:{evidence.evidence_id}"
                    finding_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

                    findings.append(
                        Finding(
                            finding_id=f"FND-{finding_hash}",
                            rule_id=self.RULE_ID,
                            category=self.RULE_CATEGORY,
                            severity=self.SEVERITY,
                            description=self.DESCRIPTION,
                            evidence=(evidence,),
                        )
                    )

        return RuleResult(
            findings=tuple(findings),
            statistics=MappingProxyType(
                {"execution_count": 1, "findings_generated": len(findings)}
            ),
        )
