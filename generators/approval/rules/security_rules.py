"""Security rules for the Approval Generator."""

import re
import hashlib
from types import MappingProxyType
from aiodoo_datasets.generators.approval.rules.base_rule import BaseRule
from aiodoo_datasets.generators.approval.rules.rule_context import RuleContext
from aiodoo_datasets.generators.approval.rules.rule_result import RuleResult
from aiodoo_datasets.generators.approval.enums import RuleCategory, Severity
from aiodoo_datasets.generators.approval.domain.finding import Finding


class SQLInjectionRule(BaseRule):  # type: ignore[misc]
    """Detects raw cr.execute calls without parameterization."""

    RULE_ID = "SEC-001"
    RULE_NAME = "SQL Injection Detection"
    RULE_CATEGORY = RuleCategory.SECURITY
    SEVERITY = Severity.CRITICAL
    DESCRIPTION = "Detects potential SQL Injection via f-strings in .execute()"
    VERSION = "1.0"
    PRIORITY = 100

    def evaluate(self, context: RuleContext) -> RuleResult:
        findings = []
        raw_execute_pattern = re.compile(r'\.execute\(\s*f["\']')

        for evidence in context.evidence_pool:
            if evidence.source_generator.value == "CODING" and evidence.snippet:
                if raw_execute_pattern.search(evidence.snippet):
                    # Deterministic finding ID
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
