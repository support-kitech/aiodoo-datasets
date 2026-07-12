"""Generator-specific validation rules for the Execution dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class ExecutionInstructionRule(BaseRule):
    """Execution record must contain a non-empty instruction."""

    @property
    def rule_id(self) -> str:
        return "EXE-001"

    @property
    def description(self) -> str:
        return "Execution record must contain a non-empty instruction."

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
        return ("execution",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        instruction = record.get("instruction", "")
        if not instruction or not isinstance(instruction, str) or not instruction.strip():
            return (
                self._issue(
                    message="Execution record has empty instruction",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="instruction",
                ),
            )
        return ()
