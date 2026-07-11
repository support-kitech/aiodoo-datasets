"""Rule: Content must be valid UTF-8 without null bytes."""

from validation.constants.framework import SERIALIZATION_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class EncodingRule(BaseRule):
    """String values should not contain null bytes."""

    @property
    def rule_id(self) -> str:
        return "SER-002"

    @property
    def description(self) -> str:
        return "String values must not contain null bytes."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.WARNING

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.SERIALIZATION

    @property
    def priority(self) -> int:
        return SERIALIZATION_RULE_PRIORITY + 1

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        issues: list[ValidationIssue] = []
        self._check_nulls(record, "", issues, context)
        return tuple(issues)

    def _check_nulls(
        self,
        obj: object,
        path: str,
        issues: list[ValidationIssue],
        context: ValidationContext,
    ) -> None:
        if isinstance(obj, str) and "\x00" in obj:
            issues.append(
                self._issue(
                    message=f"Null byte found in string at '{path}'",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path=path,
                )
            )
        elif isinstance(obj, dict):
            for key, value in obj.items():
                self._check_nulls(value, f"{path}.{key}" if path else key, issues, context)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._check_nulls(item, f"{path}[{i}]", issues, context)
