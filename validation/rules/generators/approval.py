"""Generator-specific validation rules for the Approval dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class ApprovalDecisionRule(BaseRule):
    """Approval record must contain a valid decision object."""

    @property
    def rule_id(self) -> str:
        return "APR-001"

    @property
    def description(self) -> str:
        return "Approval record must contain a valid decision."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("approval",)

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        decision = record.get("decision")
        if not isinstance(decision, dict):
            return (
                self._issue(
                    message="Approval record has missing or invalid decision object",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="decision",
                ),
            )

        issues: list[ValidationIssue] = []
        for field in ("status", "decision_id"):
            if not decision.get(field):
                issues.append(
                    self._issue(
                        message=f"Decision missing required field: '{field}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"decision.{field}",
                    )
                )
        return tuple(issues)
