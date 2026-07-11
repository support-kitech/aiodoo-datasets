"""Immutable representation of an atomic execution target."""

from dataclasses import dataclass
from typing import Any
from generators.execution.artifacts.artifact import Artifact
from generators.execution.domain.enums import OperationAction
from generators.execution.domain.types import OperationId


@dataclass(frozen=True)
class ExecutionOperation:
    """
    Defines the specific action taken against a target artifact.

    Attributes:
        operation_id: Unique deterministic string ID.
        action: The intent (Create, Update, Delete).
        target: The engineering artifact being modified.
        payload: Optional string representation of the implementation change.
    """

    operation_id: OperationId
    action: OperationAction
    target: Artifact
    payload: str | None = None

    def __hash__(self) -> int:
        return hash(self.operation_id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExecutionOperation):
            return NotImplemented
        return self.operation_id == other.operation_id  # type: ignore[no-any-return]

    def __lt__(self, other: "ExecutionOperation") -> bool:
        if not isinstance(other, ExecutionOperation):
            return NotImplemented
        return self.operation_id < other.operation_id  # type: ignore[no-any-return]
