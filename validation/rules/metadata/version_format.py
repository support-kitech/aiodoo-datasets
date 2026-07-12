"""Rule: Version strings must follow semver format."""

import re

from validation.constants.framework import METADATA_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

SEMVER_PATTERN = re.compile(r"^\d+\.\d+(\.\d+)?$")
VERSION_FIELDS = ("generator_version", "protocol_version")


class VersionFormatRule(BaseRule):
    """Version fields in metadata should follow semver-like format."""

    @property
    def rule_id(self) -> str:
        return "META-002"

    @property
    def description(self) -> str:
        return "Version fields must follow X.Y or X.Y.Z format."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.WARNING

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.METADATA

    @property
    def priority(self) -> int:
        return METADATA_RULE_PRIORITY + 1

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        metadata = record.get("metadata")
        if not isinstance(metadata, dict):
            return ()

        issues: list[ValidationIssue] = []
        for field in VERSION_FIELDS:
            value = metadata.get(field)
            if value is not None and isinstance(value, str) and not SEMVER_PATTERN.match(value):
                issues.append(
                    self._issue(
                        message=f"Invalid version format in '{field}': '{value}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"metadata.{field}",
                    )
                )
        return tuple(issues)
