"""Performance rules for the Approval Generator."""

from generators.approval.rules.base_rule import BaseRule
from generators.approval.rules.rule_context import RuleContext
from generators.approval.rules.rule_result import RuleResult
from generators.approval.enums import RuleCategory, Severity


class NPlusOneQueryRule(BaseRule):  # type: ignore[misc]
    """Detects ORM queries inside loops."""

    RULE_ID = "PERF-001"
    RULE_NAME = "N+1 Query Detection"
    RULE_CATEGORY = RuleCategory.PERFORMANCE
    SEVERITY = Severity.HIGH
    DESCRIPTION = "Detects ORM queries inside loops."
    VERSION = "1.0"
    PRIORITY = 400
    IMPLEMENTED = False

    def evaluate(self, context: RuleContext) -> RuleResult:
        # Implementation placeholder
        return RuleResult()
