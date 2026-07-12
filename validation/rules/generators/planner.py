"""Generator-specific validation rules for the Planner dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class PlannerTasksNonEmptyRule(BaseRule):
    """Planner output must contain at least one task."""

    @property
    def rule_id(self) -> str:
        return "PLN-001"

    @property
    def description(self) -> str:
        return "Planner output must contain at least one task."

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
        return ("planner",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()
        tasks = output.get("tasks", [])
        if not tasks:
            return (
                self._issue(
                    message="Planner output contains no tasks",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="output.tasks",
                ),
            )
        return ()


class PlannerGoalNonEmptyRule(BaseRule):
    """Planner output must contain a non-empty goal and summary."""

    @property
    def rule_id(self) -> str:
        return "PLN-002"

    @property
    def description(self) -> str:
        return "Planner output must contain non-empty goal and summary."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY + 1

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("planner",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        issues: list[ValidationIssue] = []
        for field in ("goal", "summary"):
            if not output.get(field):
                issues.append(
                    self._issue(
                        message=f"Planner output has empty '{field}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"output.{field}",
                    )
                )
        return tuple(issues)
