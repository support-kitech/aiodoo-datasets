"""Generator-specific validation rules for the Repair dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class RepairTaskStructureRule(BaseRule):
    """Each repair task must have problem, root_cause, and expected_outcome."""

    @property
    def rule_id(self) -> str:
        return "RPR-001"

    @property
    def description(self) -> str:
        return "Repair tasks must have problem, root_cause, and expected_outcome."

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
        return ("repair",)

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        issues: list[ValidationIssue] = []
        for i, task in enumerate(output.get("tasks", [])):
            if not isinstance(task, dict):
                continue
            for field in ("problem", "root_cause", "expected_outcome"):
                if not task.get(field):
                    issues.append(
                        self._issue(
                            message=f"Repair task {i} missing '{field}'",
                            dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                            record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                            field_path=f"output.tasks[{i}].{field}",
                        )
                    )
        return tuple(issues)


class RepairOperationsRule(BaseRule):
    """Repair operations must have search and replace fields."""

    @property
    def rule_id(self) -> str:
        return "RPR-002"

    @property
    def description(self) -> str:
        return "Operations must have search and replace fields."

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
        return ("repair",)

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        issues: list[ValidationIssue] = []
        for i, task in enumerate(output.get("tasks", [])):
            if not isinstance(task, dict):
                continue
            outcome = task.get("expected_outcome", {})
            if not isinstance(outcome, dict):
                continue
            for j, op in enumerate(outcome.get("operations", [])):
                if not isinstance(op, dict):
                    continue
                if "search" not in op or "replace" not in op:
                    issues.append(
                        self._issue(
                            message=f"Operation {j} in task {i} missing search/replace",
                            dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                            record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                            field_path=f"output.tasks[{i}].expected_outcome.operations[{j}]",
                        )
                    )
        return tuple(issues)
