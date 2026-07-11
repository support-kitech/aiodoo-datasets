"""Generator-specific validation rules for the Coding dataset."""

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class CodingArtifactsNonEmptyRule(BaseRule):
    """Coding output must contain at least one artifact."""

    @property
    def rule_id(self) -> str:
        return "COD-001"

    @property
    def description(self) -> str:
        return "Coding output must contain at least one artifact."

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
        return ("coding",)

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()
        if not output.get("artifacts"):
            return (
                self._issue(
                    message="Coding output contains no artifacts",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="output.artifacts",
                ),
            )
        return ()


class CodingArtifactValidPathRule(BaseRule):
    """Every coding artifact must have a valid path and language."""

    @property
    def rule_id(self) -> str:
        return "COD-002"

    @property
    def description(self) -> str:
        return "Artifacts must have valid path and language."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY + 1

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("coding",)

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        issues: list[ValidationIssue] = []
        for i, artifact in enumerate(output.get("artifacts", [])):
            if not isinstance(artifact, dict):
                continue
            if not artifact.get("path"):
                issues.append(
                    self._issue(
                        message=f"Artifact at index {i} has empty path",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"output.artifacts[{i}].path",
                    )
                )
        return tuple(issues)
