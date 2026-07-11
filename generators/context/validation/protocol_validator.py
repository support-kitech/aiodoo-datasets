"""Protocol Validator for Context Protocol V1."""

import logging

from generators.context.protocol.schema import ContextTask
from generators.context.validation.result import ValidationResult

logger = logging.getLogger(__name__)


class ProtocolValidator:
    """
    Validates Protocol semantic invariants.
    Ensures logically correct datasets (e.g. no missing IDs, scores 0-100).
    Never modifies data.
    """

    def validate(self, task: ContextTask) -> ValidationResult:
        """
        Validates protocol-level semantic invariants.

        Args:
            task: The ContextTask to validate.

        Returns:
            ValidationResult containing status and any errors.
        """
        is_valid = True
        errors = []

        # Validate Query
        if not task.query.query_id:
            msg = f"Empty Query ID in Task {task.id}"
            logger.error("Protocol Validation Failed: %s", msg)
            errors.append(msg)
            is_valid = False

        if not task.query.target_node:
            msg = f"Empty Target Node in Query {task.query.query_id}"
            logger.error("Protocol Validation Failed: %s", msg)
            errors.append(msg)
            is_valid = False

        # Validate Artifacts
        seen_artifact_ids = set()
        for artifact in task.artifacts:
            if not artifact.node_id:
                msg = "Missing node_id in artifact"
                logger.error("Protocol Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False

            if artifact.node_id in seen_artifact_ids:
                msg = f"Duplicate artifact node_id {artifact.node_id}"
                logger.error("Protocol Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False
            seen_artifact_ids.add(artifact.node_id)

            if not (0 <= artifact.score <= 100):
                msg = f"Invalid score {artifact.score} for artifact {artifact.node_id}"
                logger.error("Protocol Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False

        # Validate Graph References
        graph_node_ids = {node.node_id for node in task.graph.nodes}
        for artifact in task.artifacts:
            if artifact.node_id not in graph_node_ids:
                msg = f"Artifact {artifact.node_id} not in graph nodes"
                logger.error("Protocol Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False

        if task.query.target_node not in graph_node_ids:
            msg = f"Target node {task.query.target_node} not in graph nodes"
            logger.error("Protocol Validation Failed: %s", msg)
            errors.append(msg)
            is_valid = False

        # Validate Edges point to existing nodes
        seen_edges = set()
        for edge in task.graph.edges:
            if edge.source_id not in graph_node_ids or edge.target_id not in graph_node_ids:
                msg = f"Edge {edge.edge_id} references missing nodes"
                logger.error("Protocol Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False

            if edge.edge_id in seen_edges:
                msg = f"Duplicate edge {edge.edge_id}"
                logger.error("Protocol Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False
            seen_edges.add(edge.edge_id)

        return ValidationResult(valid=is_valid, validator=self.__class__.__name__, errors=errors)
