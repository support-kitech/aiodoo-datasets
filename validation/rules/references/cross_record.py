"""Rule: Cross-record references should be internally consistent."""

from validation.constants.framework import REFERENCE_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class CrossRecordReferenceRule(BaseRule):
    """Placeholder for cross-record reference validation. Operates at dataset level."""

    @property
    def rule_id(self) -> str:
        return "REF-003"

    @property
    def description(self) -> str:
        return "Cross-record references must be internally consistent."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.WARNING

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.REFERENCES

    @property
    def priority(self) -> int:
        return REFERENCE_RULE_PRIORITY + 2

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        # Cross-record validation is handled by CrossDatasetValidator
        return ()
