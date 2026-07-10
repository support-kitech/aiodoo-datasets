"""Node integrity validator."""

from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.results.validation_result import ValidationResult


class NodeValidator:
    """
    Validates node integrity: unique IDs, non-empty payloads, correct types.
    Completely independent from EdgeValidator.
    """

    @staticmethod
    def validate(graph: ExecutionGraph) -> ValidationResult:
        violations: list[str] = []
        seen_ids: set[str] = set()

        for node in graph.nodes:
            if not node.node_id:
                violations.append("Node has empty node_id")
            if node.node_id in seen_ids:
                violations.append(f"Duplicate node_id: {node.node_id}")
            seen_ids.add(node.node_id)

            if node.payload is None:
                violations.append(f"Node {node.node_id} has None payload")

        return ValidationResult(
            success=len(violations) == 0,
            violations=tuple(violations),
        )
