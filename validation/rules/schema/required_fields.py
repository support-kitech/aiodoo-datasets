"""Rule: Required fields must be present according to the resolved schema."""

from validation.constants.framework import SCHEMA_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

# Fallback for unknown generators (backward compatible)
_FALLBACK_REQUIRED = ("instruction", "output", "metadata")


class RequiredFieldsRule(BaseRule):
    """Every dataset record must contain all required fields defined by its schema."""

    @property
    def rule_id(self) -> str:
        return "SCH-001"

    @property
    def description(self) -> str:
        return "Required fields (per generator schema) must be present."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.FATAL

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.SCHEMA

    @property
    def priority(self) -> int:
        return SCHEMA_RULE_PRIORITY

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        schema = context.metadata.get("resolved_schema")
        ds_name = context.metadata.get("current_dataset", "")
        rec_idx = context.metadata.get("current_index")

        if schema is not None:
            required_keys = schema.required_field_names
        else:
            required_keys = frozenset(_FALLBACK_REQUIRED)

        issues: list[ValidationIssue] = []
        for key in sorted(required_keys):
            if key not in record:
                issues.append(
                    self._issue(
                        message=f"Missing required field: '{key}'",
                        dataset_name=ds_name,  # type: ignore[arg-type]
                        record_index=rec_idx,  # type: ignore[arg-type]
                        field_path=key,
                    )
                )
        return tuple(issues)
