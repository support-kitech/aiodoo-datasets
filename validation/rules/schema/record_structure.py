"""Rule: Record structure must only contain fields allowed by the resolved schema."""

from validation.constants.framework import SCHEMA_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

_FALLBACK_ALLOWED = frozenset({"instruction", "input", "context", "output", "metadata"})


class RecordStructureRule(BaseRule):
    """Records should only contain fields defined in the resolved schema."""

    @property
    def rule_id(self) -> str:
        return "SCH-003"

    @property
    def description(self) -> str:
        return "Record must only contain fields allowed by its schema."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.SCHEMA

    @property
    def priority(self) -> int:
        return SCHEMA_RULE_PRIORITY + 2

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        schema = context.metadata.get("resolved_schema")

        if schema is not None:
            allowed = schema.all_field_names
        else:
            allowed = _FALLBACK_ALLOWED

        unexpected = set(record.keys()) - allowed
        if unexpected:
            return (
                self._issue(
                    message=f"Unexpected top-level keys: {sorted(unexpected)}",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                ),
            )
        return ()
