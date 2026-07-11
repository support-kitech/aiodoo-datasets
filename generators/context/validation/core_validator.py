"""Core Validator for Context Protocol V1."""

import logging

from generators.context.protocol.schema import ContextTask
from generators.context.protocol.constants import CONTEXT_PROTOCOL_V1
from generators.context.validation.result import ValidationResult

logger = logging.getLogger(__name__)


class CoreValidator:
    """
    Validates dataset-wide deterministic guarantees.
    Ensures strict determinism, correct protocol versions, and proper metadata.
    Never modifies data.
    """

    def validate(self, task: ContextTask) -> ValidationResult:
        """
        Validates core deterministic dataset rules.

        Args:
            task: The ContextTask to validate.

        Returns:
            ValidationResult containing status and any errors.
        """
        is_valid = True
        errors = []

        # Protocol Version
        if task.metadata.protocol_version != CONTEXT_PROTOCOL_V1:
            msg = f"Invalid Protocol Version {task.metadata.protocol_version}"
            logger.error("Core Validation Failed: %s", msg)
            errors.append(msg)
            is_valid = False

        # Metadata completeness matching actual content
        if task.metadata.artifact_count != len(task.artifacts):
            msg = f"Artifact count mismatch. Meta: {task.metadata.artifact_count}, Actual: {len(task.artifacts)}"
            logger.error("Core Validation Failed: %s", msg)
            errors.append(msg)
            is_valid = False

        if task.metadata.relationship_count != len(task.graph.edges):
            msg = f"Relationship count mismatch. Meta: {task.metadata.relationship_count}, Actual: {len(task.graph.edges)}"
            logger.error("Core Validation Failed: %s", msg)
            errors.append(msg)
            is_valid = False

        # Deterministic Ordering Verification
        # 1. Artifacts must be sorted by score DESC, node_id ASC
        for i in range(len(task.artifacts) - 1):
            a1 = task.artifacts[i]
            a2 = task.artifacts[i + 1]
            if a1.score < a2.score:
                msg = f"Artifacts out of order by score. {a1.score} < {a2.score}"
                logger.error("Core Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False
            elif a1.score == a2.score:
                if a1.node_id > a2.node_id:
                    msg = f"Artifacts out of order by node_id. {a1.node_id} > {a2.node_id}"
                    logger.error("Core Validation Failed: %s", msg)
                    errors.append(msg)
                    is_valid = False

        # 2. Nodes sorted by node_id ASC
        for i in range(len(task.graph.nodes) - 1):
            n1 = task.graph.nodes[i]
            n2 = task.graph.nodes[i + 1]
            if n1.node_id > n2.node_id:
                msg = f"Nodes out of order. {n1.node_id} > {n2.node_id}"
                logger.error("Core Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False

        # 3. Edges sorted by edge_id ASC
        for i in range(len(task.graph.edges) - 1):
            e1 = task.graph.edges[i]
            e2 = task.graph.edges[i + 1]
            if e1.edge_id > e2.edge_id:
                msg = f"Edges out of order. {e1.edge_id} > {e2.edge_id}"
                logger.error("Core Validation Failed: %s", msg)
                errors.append(msg)
                is_valid = False

        return ValidationResult(valid=is_valid, validator=self.__class__.__name__, errors=errors)
