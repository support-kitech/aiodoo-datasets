"""Graph validation orchestrator."""

from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.results.validation_result import ValidationResult
from generators.execution.validation.node_validator import NodeValidator
from generators.execution.validation.edge_validator import EdgeValidator


class GraphValidator:
    """
    Orchestrates node and edge validators.
    Contains no validation logic itself.
    """

    @staticmethod
    def validate(graph: ExecutionGraph) -> ValidationResult:
        node_result = NodeValidator.validate(graph)
        edge_result = EdgeValidator.validate(graph)

        all_violations = node_result.violations + edge_result.violations

        return ValidationResult(
            success=node_result.success and edge_result.success,
            violations=all_violations,
        )
