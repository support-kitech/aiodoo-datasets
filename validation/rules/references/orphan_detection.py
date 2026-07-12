"""Rule: Dependency references within a record must resolve."""

from validation.constants.framework import REFERENCE_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class OrphanReferenceRule(BaseRule):
    """Artifact dependency IDs must reference other artifacts in the same record."""

    @property
    def rule_id(self) -> str:
        return "REF-001"

    @property
    def description(self) -> str:
        return "Dependency IDs must resolve within the record."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.REFERENCES

    @property
    def priority(self) -> int:
        return REFERENCE_RULE_PRIORITY

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        artifacts = output.get("artifacts", [])
        if not isinstance(artifacts, list):
            return ()

        known_ids = {a.get("id") for a in artifacts if isinstance(a, dict) and a.get("id")}
        issues: list[ValidationIssue] = []

        for i, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                continue
            deps = artifact.get("dependencies", [])
            if not isinstance(deps, list):
                continue
            for dep_id in deps:
                if dep_id not in known_ids:
                    issues.append(
                        self._issue(
                            message=f"Artifact '{artifact.get('id', '?')}' references unknown dependency: '{dep_id}'",
                            dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                            record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                            field_path=f"output.artifacts[{i}].dependencies",
                        )
                    )

        return tuple(issues)
