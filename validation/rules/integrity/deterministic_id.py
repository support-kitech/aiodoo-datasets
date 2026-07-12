"""Rule: Task and artifact IDs must be non-empty strings."""

from validation.constants.framework import INTEGRITY_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class DeterministicIdRule(BaseRule):
    """IDs within output payloads must be non-empty strings."""

    @property
    def rule_id(self) -> str:
        return "INT-003"

    @property
    def description(self) -> str:
        return "Task and artifact IDs must be non-empty."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.INTEGRITY

    @property
    def priority(self) -> int:
        return INTEGRITY_RULE_PRIORITY + 2

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        issues: list[ValidationIssue] = []
        ds_name = context.metadata.get("current_dataset", "")
        rec_idx = context.metadata.get("current_index")

        # Check tasks
        for i, task in enumerate(output.get("tasks", [])):
            if isinstance(task, dict) and not task.get("id"):
                issues.append(
                    self._issue(
                        message=f"Task at index {i} has empty or missing ID",
                        dataset_name=ds_name,  # type: ignore[arg-type]
                        record_index=rec_idx,  # type: ignore[arg-type]
                        field_path=f"output.tasks[{i}].id",
                    )
                )

        # Check artifacts
        for i, artifact in enumerate(output.get("artifacts", [])):
            if isinstance(artifact, dict) and not artifact.get("id"):
                issues.append(
                    self._issue(
                        message=f"Artifact at index {i} has empty or missing ID",
                        dataset_name=ds_name,  # type: ignore[arg-type]
                        record_index=rec_idx,  # type: ignore[arg-type]
                        field_path=f"output.artifacts[{i}].id",
                    )
                )

        return tuple(issues)
