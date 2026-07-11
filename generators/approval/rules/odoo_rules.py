"""Odoo specific rules for the Approval Generator."""

from aiodoo_datasets.generators.approval.rules.base_rule import BaseRule
from aiodoo_datasets.generators.approval.rules.rule_context import RuleContext
from aiodoo_datasets.generators.approval.rules.rule_result import RuleResult
from aiodoo_datasets.generators.approval.enums import RuleCategory, Severity


class OdooManifestRule(BaseRule):
    """Validates the presence and format of __manifest__.py."""

    RULE_ID = "ODOO-001"
    RULE_NAME = "Odoo Manifest Validation"
    RULE_CATEGORY = RuleCategory.ODOO
    SEVERITY = Severity.HIGH
    DESCRIPTION = "Validates the presence and format of __manifest__.py."
    VERSION = "1.0"
    PRIORITY = 500
    IMPLEMENTED = False

    def evaluate(self, context: RuleContext) -> RuleResult:
        # Implementation placeholder
        return RuleResult()
