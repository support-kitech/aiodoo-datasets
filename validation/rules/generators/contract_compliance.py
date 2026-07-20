"""Contract compliance rules: does a record project onto `aiodoo_contract`?

Phase 2 ("AIODOO Ecosystem v2.0.0-fixes — aiodoo-datasets Contract
Adoption") requires structural validation to use `aiodoo_contract.validators`
where an equivalent check does not already exist in this framework (see
`CONTRACT_ADOPTION.md`). The existing generator-specific rules in this
package (`RepairTaskStructureRule`, `ApprovalDecisionRule`, ...) check this
repository's own row-level envelope (`instruction`/`context`/`output`/
`metadata`), which is *not* an `aiodoo_contract` concern — the contract only
defines the shape of a capability's request/response. These rules are the
complement: they project a record onto its canonical
`aiodoo_contract` request/response pair
(:mod:`generators.common.contract.adapters`) and run it through
`aiodoo_contract.validators.ContractValidator`.

Severity is deliberately `WARNING`, not `ERROR`: a record that cannot yet be
projected onto the contract (e.g. a coding artifact with no file content) is
a known, tracked data-richness gap (see CONTRACT_ADOPTION.md), not a
structural defect that should fail a `build_dataset.py` run. This mirrors
`RecordValidator`'s existing policy that only `fatal`/`error` severities fail
a dataset (`validation/validators/record_validator.py`).
"""

from __future__ import annotations

from aiodoo_contract.validators import ContractValidator

from generators.common.contract.adapters import ContractAdapterError, project_record
from validation.constants.framework import CONTRACT_RULE_PRIORITY
from validation.domain.enums import RuleScope, ValidationCategory, ValidationSeverity
from validation.domain.models import ValidationContext, ValidationIssue
from validation.rules.base import BaseRule

__all__ = ["ContractComplianceRule", "build_contract_compliance_rules"]

_contract_validator = ContractValidator()


class ContractComplianceRule(BaseRule):
    """Checks that one capability's record projects onto `aiodoo_contract`.

    One instance is registered per capability (see
    :func:`build_contract_compliance_rules`) so each carries a distinct,
    stable ``rule_id`` and only targets its own generator's dataset.
    """

    def __init__(self, capability: str, rule_id: str) -> None:
        self._capability = capability
        self._rule_id = rule_id

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @property
    def description(self) -> str:
        return (
            f"{self._capability} records should project onto the canonical "
            f"aiodoo_contract request/response schema."
        )

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.WARNING

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.CONTRACT

    @property
    def priority(self) -> int:
        return CONTRACT_RULE_PRIORITY

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return (self._capability,)

    def validate(
        self,
        record: dict,  # type: ignore[type-arg]
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        try:
            projection = project_record(self._capability, record)
        except ContractAdapterError as exc:
            return (
                self._issue(
                    message=f"Could not project onto aiodoo_contract: {exc}",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="",
                ),
            )

        request_result = _contract_validator.validate_request(projection.request)
        response_result = _contract_validator.validate_response(projection.response)

        issues: list[ValidationIssue] = []
        for label, result in (("request", request_result), ("response", response_result)):
            if not result.valid:
                for contract_issue in result.issues:
                    issues.append(
                        self._issue(
                            message=f"aiodoo_contract {label} validation: {contract_issue.message}",
                            dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                            record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                            field_path=contract_issue.path,
                        )
                    )
        return tuple(issues)


def build_contract_compliance_rules() -> tuple[ContractComplianceRule, ...]:
    """Build one `ContractComplianceRule` per supported capability."""
    from generators.common.contract.adapters import SUPPORTED_CAPABILITIES

    return tuple(
        ContractComplianceRule(capability=capability, rule_id=f"CTR-{index:03d}")
        for index, capability in enumerate(sorted(SUPPORTED_CAPABILITIES), start=1)
    )
