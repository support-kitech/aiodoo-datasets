"""Rule: Required metadata fields must be present per the resolved schema."""

from validation.constants.framework import METADATA_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

_FALLBACK_METADATA_KEYS = ("protocol_hash", "module")


class RequiredMetadataRule(BaseRule):
    """Metadata dict must contain required fields per the resolved schema."""

    @property
    def rule_id(self) -> str:
        return "META-001"

    @property
    def description(self) -> str:
        return "Metadata must contain required fields per generator schema."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.METADATA

    @property
    def priority(self) -> int:
        return METADATA_RULE_PRIORITY

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        metadata = record.get("metadata")
        if not isinstance(metadata, dict):
            return ()  # SCH-002 handles type issues

        schema = context.metadata.get("resolved_schema")
        if schema is not None:
            required_keys = schema.metadata_required_fields
        else:
            required_keys = _FALLBACK_METADATA_KEYS

        issues: list[ValidationIssue] = []
        for key in required_keys:
            if key not in metadata or not metadata[key]:
                issues.append(
                    self._issue(
                        message=f"Missing required metadata field: '{key}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"metadata.{key}",
                    )
                )
        return tuple(issues)
