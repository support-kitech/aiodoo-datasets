"""Edge integrity validator."""

from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.results.validation_result import ValidationResult


class EdgeValidator:
    """
    Validates edge integrity: valid source/target references, no self-loops, no duplicate edges.
    Completely independent from NodeValidator.
    """

    @staticmethod
    def validate(graph: ExecutionGraph) -> ValidationResult:
        violations: list[str] = []
        node_ids = {n.node_id for n in graph.nodes}
        seen_edges: set[tuple[str, str]] = set()

        for edge in graph.edges:
            # Self-loop check
            if edge.source_id == edge.target_id:
                violations.append(f"Self-loop detected: {edge.source_id}")

            # Referential integrity
            if edge.source_id not in node_ids:
                violations.append(f"Edge source {edge.source_id} references non-existent node")
            if edge.target_id not in node_ids:
                violations.append(f"Edge target {edge.target_id} references non-existent node")

            # Duplicate edge check
            edge_key = (edge.source_id, edge.target_id)
            if edge_key in seen_edges:
                violations.append(f"Duplicate edge: {edge.source_id} -> {edge.target_id}")
            seen_edges.add(edge_key)

        return ValidationResult(
            success=len(violations) == 0,
            violations=tuple(violations),
        )
