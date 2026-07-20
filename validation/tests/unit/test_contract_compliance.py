"""Unit tests for `ContractComplianceRule` (validation/rules/generators/contract_compliance.py).

Covers Phase 2's integration of `aiodoo_contract.validators` into the
validation framework: a contract-conformant record produces zero issues, a
record that cannot be projected (adapter error) or fails contract validation
produces WARNING-severity `ValidationCategory.CONTRACT` issues, and one rule
instance is generated per supported capability.
"""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType

from validation.domain.enums import RuleScope, ValidationCategory, ValidationSeverity
from validation.domain.models import ValidationContext
from validation.rules.generators.contract_compliance import (
    ContractComplianceRule,
    build_contract_compliance_rules,
)


def _ctx(dataset: str = "test.jsonl", index: int = 0) -> ValidationContext:
    return ValidationContext(
        dataset_dir=Path("."),
        metadata=MappingProxyType({"current_dataset": dataset, "current_index": index}),
    )


class TestBuildContractComplianceRules:
    def test_one_rule_per_supported_capability(self) -> None:
        from generators.common.contract.adapters import SUPPORTED_CAPABILITIES

        rules = build_contract_compliance_rules()

        assert len(rules) == len(SUPPORTED_CAPABILITIES)
        assert {rule.target_generators[0] for rule in rules} == set(SUPPORTED_CAPABILITIES)

    def test_rule_ids_are_stable_and_unique(self) -> None:
        rules = build_contract_compliance_rules()

        rule_ids = [rule.rule_id for rule in rules]
        assert len(rule_ids) == len(set(rule_ids))
        assert all(rule_id.startswith("CTR-") for rule_id in rule_ids)


class TestContractComplianceRuleMetadata:
    def setup_method(self) -> None:
        self.rule = ContractComplianceRule(capability="repair", rule_id="CTR-TEST")

    def test_severity_is_warning_not_error(self) -> None:
        assert self.rule.severity is ValidationSeverity.WARNING

    def test_category_is_contract(self) -> None:
        assert self.rule.category is ValidationCategory.CONTRACT

    def test_scope_is_generator_specific_to_its_capability(self) -> None:
        assert self.rule.scope is RuleScope.GENERATOR_SPECIFIC
        assert self.rule.target_generators == ("repair",)


class TestContractComplianceRuleValidatePlanner:
    def setup_method(self) -> None:
        self.rule = ContractComplianceRule(capability="planner", rule_id="CTR-TEST")

    def test_conformant_record_produces_no_issues(self) -> None:
        record = {
            "instruction": "Build feature X",
            "input": "Target Odoo Version: 17.0",
            "output": {
                "goal": "Build feature X",
                "tasks": [{"id": "t1", "title": "Create model", "priority": "medium"}],
            },
        }
        issues = self.rule.validate(record, _ctx())
        assert issues == ()

    def test_unprojectable_record_produces_warning_issue(self) -> None:
        record = {"instruction": "x"}  # no "output" -> adapter cannot project

        issues = self.rule.validate(record, _ctx(dataset="planner.jsonl", index=3))

        assert len(issues) == 1
        issue = issues[0]
        assert issue.rule_id == "CTR-TEST"
        assert issue.severity is ValidationSeverity.WARNING
        assert issue.category is ValidationCategory.CONTRACT
        assert issue.dataset_name == "planner.jsonl"
        assert issue.record_index == 3
        assert "Could not project onto aiodoo_contract" in issue.message


class TestContractComplianceRuleValidateRepair:
    def setup_method(self) -> None:
        self.rule = ContractComplianceRule(capability="repair", rule_id="CTR-TEST")

    def test_conformant_record_produces_no_issues(self) -> None:
        record = {
            "instruction": "Fix the bug.",
            "output": {
                "tasks": [
                    {
                        "problem": {
                            "description": "Direct SQL bypasses ORM rules.",
                            "severity": "high",
                        },
                        "root_cause": {"analysis": "cr.execute used directly."},
                        "artifacts": [
                            {"path": "models/foo.py", "content": "self.env.cr.execute(x)"}
                        ],
                        "expected_outcome": {
                            "operations": [
                                {
                                    "operation": "replace",
                                    "search": "self.env.cr.execute",
                                    "replace": "self.env.sudo().cr.execute",
                                }
                            ]
                        },
                    }
                ]
            },
        }
        issues = self.rule.validate(record, _ctx())
        assert issues == ()

    def test_record_with_no_tasks_produces_warning_issue(self) -> None:
        record: dict[str, object] = {"output": {"tasks": []}}

        issues = self.rule.validate(record, _ctx())

        assert len(issues) == 1
        assert issues[0].severity is ValidationSeverity.WARNING
