"""Rule: No circular dependencies in task/artifact graphs."""

from validation.constants.framework import REFERENCE_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class CircularReferenceRule(BaseRule):
    """Detects circular dependencies in artifact dependency graphs."""

    @property
    def rule_id(self) -> str:
        return "REF-002"

    @property
    def description(self) -> str:
        return "No circular dependencies in task/artifact graphs."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.REFERENCES

    @property
    def priority(self) -> int:
        return REFERENCE_RULE_PRIORITY + 1

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return ()

        artifacts = output.get("artifacts", [])
        if not isinstance(artifacts, list):
            return ()

        # Build adjacency list
        graph: dict[str, list[str]] = {}
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                continue
            aid = artifact.get("id", "")
            deps = artifact.get("dependencies", [])
            if aid and isinstance(deps, list):
                graph[aid] = [d for d in deps if isinstance(d, str)]

        # DFS cycle detection
        visited: set[str] = set()
        in_stack: set[str] = set()

        def has_cycle(node: str) -> bool:
            if node in in_stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            in_stack.add(node)
            for neighbor in graph.get(node, []):
                if has_cycle(neighbor):
                    return True
            in_stack.discard(node)
            return False

        for node_id in graph:
            if has_cycle(node_id):
                return (
                    self._issue(
                        message=f"Circular dependency detected involving: '{node_id}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path="output.artifacts",
                    ),
                )

        return ()
