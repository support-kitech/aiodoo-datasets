"""Rule: Timestamp fields must follow ISO 8601 format."""

import re

from validation.constants.framework import METADATA_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

ISO8601_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


class TimestampFormatRule(BaseRule):
    """Timestamp fields must follow ISO 8601 format."""

    @property
    def rule_id(self) -> str:
        return "META-003"

    @property
    def description(self) -> str:
        return "Timestamps must follow ISO 8601 format."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.WARNING

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.METADATA

    @property
    def priority(self) -> int:
        return METADATA_RULE_PRIORITY + 2

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        metadata = record.get("metadata")
        if not isinstance(metadata, dict):
            return ()

        ts = metadata.get("generation_timestamp")
        if ts is not None and isinstance(ts, str) and not ISO8601_PATTERN.match(ts):
            return (
                self._issue(
                    message=f"Invalid timestamp format: '{ts}'",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="metadata.generation_timestamp",
                ),
            )
        return ()
