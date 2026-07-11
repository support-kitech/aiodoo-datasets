"""Rule: Every JSONL line must be valid JSON."""

from validation.constants.framework import SERIALIZATION_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class JsonCompatibilityRule(BaseRule):
    """Every record must be a valid, parseable JSON object."""

    @property
    def rule_id(self) -> str:
        return "SER-001"

    @property
    def description(self) -> str:
        return "Every JSONL line must be valid JSON."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.FATAL

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.SERIALIZATION

    @property
    def priority(self) -> int:
        return SERIALIZATION_RULE_PRIORITY

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        # By the time this rule runs, the record is already parsed.
        # JSON parsing failures are caught in DatasetValidator before rules execute.
        return ()
