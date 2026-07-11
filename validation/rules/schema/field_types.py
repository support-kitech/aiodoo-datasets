"""Rule: Field types must match the resolved schema's type definitions."""

from validation.constants.framework import SCHEMA_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

# Fallback for unknown generators
_FALLBACK_TYPES = {
    "instruction": str,
    "output": dict,
    "metadata": dict,
}


class FieldTypeRule(BaseRule):
    """Top-level fields must have the correct types per the resolved schema."""

    @property
    def rule_id(self) -> str:
        return "SCH-002"

    @property
    def description(self) -> str:
        return "Top-level field types must match schema expectations."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.SCHEMA

    @property
    def priority(self) -> int:
        return SCHEMA_RULE_PRIORITY + 1

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        schema = context.metadata.get("resolved_schema")
        ds_name = context.metadata.get("current_dataset", "")
        rec_idx = context.metadata.get("current_index")

        if schema is not None:
            type_map = {
                f.name: f.field_type for f in schema.top_level_fields if f.field_type is not object
            }
        else:
            type_map = _FALLBACK_TYPES

        issues: list[ValidationIssue] = []
        for field_name, expected_type in type_map.items():
            value = record.get(field_name)
            if value is not None and not isinstance(value, expected_type):
                expected_name = (
                    expected_type.__name__
                    if isinstance(expected_type, type)
                    else str(expected_type)
                )
                issues.append(
                    self._issue(
                        message=f"Field '{field_name}' expected {expected_name}, got {type(value).__name__}",
                        dataset_name=ds_name,  # type: ignore[arg-type]
                        record_index=rec_idx,  # type: ignore[arg-type]
                        field_path=field_name,
                    )
                )
        return tuple(issues)
