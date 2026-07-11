"""Rule system for the Approval Generator."""

from generators.approval.rules.registry import RuleRegistry
from generators.approval.rules.architecture_rules import DependencyCycleRule
from generators.approval.rules.security_rules import SQLInjectionRule
from generators.approval.rules.performance_rules import NPlusOneQueryRule
from generators.approval.rules.style_rules import Pep8ComplianceRule
from generators.approval.rules.odoo_rules import OdooManifestRule
from generators.approval.rules.protocol_rules import ProtocolIntegrityRule


def register_all_rules():  # type: ignore[no-untyped-def]
    RuleRegistry.register(SQLInjectionRule)
    RuleRegistry.register(Pep8ComplianceRule)
    RuleRegistry.register(DependencyCycleRule)
    RuleRegistry.register(NPlusOneQueryRule)
    RuleRegistry.register(OdooManifestRule)
    RuleRegistry.register(ProtocolIntegrityRule)


register_all_rules()  # type: ignore[no-untyped-call]
