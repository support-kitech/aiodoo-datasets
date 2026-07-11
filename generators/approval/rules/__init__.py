"""Rule system for the Approval Generator."""

from aiodoo_datasets.generators.approval.rules.registry import RuleRegistry
from aiodoo_datasets.generators.approval.rules.architecture_rules import DependencyCycleRule
from aiodoo_datasets.generators.approval.rules.security_rules import SQLInjectionRule
from aiodoo_datasets.generators.approval.rules.performance_rules import NPlusOneQueryRule
from aiodoo_datasets.generators.approval.rules.style_rules import Pep8ComplianceRule
from aiodoo_datasets.generators.approval.rules.odoo_rules import OdooManifestRule
from aiodoo_datasets.generators.approval.rules.protocol_rules import ProtocolIntegrityRule


def register_all_rules():
    RuleRegistry.register(SQLInjectionRule)
    RuleRegistry.register(Pep8ComplianceRule)
    RuleRegistry.register(DependencyCycleRule)
    RuleRegistry.register(NPlusOneQueryRule)
    RuleRegistry.register(OdooManifestRule)
    RuleRegistry.register(ProtocolIntegrityRule)


register_all_rules()
