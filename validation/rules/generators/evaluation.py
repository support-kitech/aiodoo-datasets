"""Generator-specific validation rules for the Evaluation dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class EvaluationCatalogRule(BaseRule):
    """Evaluation record must contain a valid catalog object."""

    @property
    def rule_id(self) -> str:
        return "EVL-001"

    @property
    def description(self) -> str:
        return "Evaluation record must contain a valid catalog."

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
        return ("evaluation",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        catalog = record.get("catalog")
        if not isinstance(catalog, dict):
            return (
                self._issue(
                    message="Evaluation record has missing or invalid catalog object",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="catalog",
                ),
            )

        issues: list[ValidationIssue] = []
        for field in ("catalog_id", "catalog_name"):
            if not catalog.get(field):
                issues.append(
                    self._issue(
                        message=f"Catalog missing required field: '{field}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"catalog.{field}",
                    )
                )
        return tuple(issues)
