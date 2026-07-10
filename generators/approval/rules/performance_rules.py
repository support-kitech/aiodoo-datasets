"""Performance rules for the Approval Generator."""

from aiodoo_datasets.generators.approval.rules.base_rule import BaseRule
from aiodoo_datasets.generators.approval.rules.rule_context import RuleContext
from aiodoo_datasets.generators.approval.rules.rule_result import RuleResult
from aiodoo_datasets.generators.approval.enums import RuleCategory, Severity

class NPlusOneQueryRule(BaseRule):
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
