"""Wrapper to integrate AIODOO Core Protocol Validator into the Repair Datasets pipeline."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CoreProtocolValidator:
    """Pluggable adapter for AIODOO Core V1 validation."""

    def __init__(self):
        # We don't strictly bind to the AIODOO Core Protocol Validator for Repair
        # because Repair uses a specialized protocol schema specifically for training.
        pass

    def validate_payload(self, payload_dict: dict[str, Any]) -> None:
        """Validates a raw dataset output dictionary against engineering invariants."""
        tasks = payload_dict.get("tasks", [])

        task_ids = set()
        for task in tasks:
            t_id = task.get("id")
            if not t_id:
                raise ValueError("RepairTask is missing an ID")
            if t_id in task_ids:
                raise ValueError(f"Duplicate task ID found: {t_id}")
            task_ids.add(t_id)

            # Ensure expected outcome has operations
            outcome = task.get("expected_outcome", {})
            operations = outcome.get("operations", [])
            if not operations:
                raise ValueError(f"RepairTask {t_id} is missing expected operations")
            for op in operations:
                if not op.get("operation") or "search" not in op or "replace" not in op:
                    raise ValueError(f"RepairTask {t_id} has an invalid operation format")

            # Ensure artifacts list has content
            artifacts = task.get("artifacts", [])
            for art in artifacts:
                if not art.get("path") or not art.get("content"):
                    raise ValueError(f"RepairTask {t_id} contains an invalid artifact")
