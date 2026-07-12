"""Generator-specific validation rules for the Context dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class ContextQueryRule(BaseRule):
    """Context records must contain a non-empty query with required subfields."""

    @property
    def rule_id(self) -> str:
        return "CTX-001"

    @property
    def description(self) -> str:
        return "Context record must have a valid query object."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("context",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        query = record.get("query")
        if not isinstance(query, dict):
            return (
                self._issue(
                    message="Context record has missing or invalid query object",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="query",
                ),
            )

        issues: list[ValidationIssue] = []
        for field in ("query_id", "natural_language"):
            if not query.get(field):
                issues.append(
                    self._issue(
                        message=f"Query missing required field: '{field}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"query.{field}",
                    )
                )
        return tuple(issues)
