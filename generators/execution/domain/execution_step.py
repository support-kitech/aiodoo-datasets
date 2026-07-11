"""Immutable representation of a complete execution step."""

from dataclasses import dataclass, field
from typing import Any
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation
from aiodoo_datasets.generators.execution.domain.execution_dependency import ExecutionDependency
from aiodoo_datasets.generators.execution.domain.execution_constraint import ExecutionConstraint
from aiodoo_datasets.generators.execution.domain.execution_verification import ExecutionVerification
from aiodoo_datasets.generators.execution.domain.execution_rollback import ExecutionRollback
from aiodoo_datasets.generators.execution.domain.execution_metadata import ExecutionMetadata
from aiodoo_datasets.generators.execution.domain.types import StepId
from aiodoo_datasets.generators.execution.domain.constants import (
    DEFAULT_PRIORITY,
    EMPTY_DEPENDENCIES,
    EMPTY_CONSTRAINTS,
    EMPTY_VERIFICATIONS,
    EMPTY_ROLLBACKS,
    EMPTY_TAGS,
)


@dataclass(frozen=True)
class ExecutionStep:
    """
    An atomic, isolated block of execution aggregating an operation with its dependencies and recovery mechanics.

    Attributes:
        step_id: Unique deterministic SHA-256 identifier.
        description: Natural language summary of the step.
        operation: The core implementation payload.
        priority: Deterministic ordering priority.
        tags: Metadata tags for filtering.
        metadata: Execution metadata excluded from hashing.
        dependencies: Tuple of prerequisite steps.
        constraints: Tuple of required conditions.
        verifications: Tuple of success assertions.
        rollbacks: Tuple of failure recovery commands.
    """

    step_id: StepId
    description: str
    operation: ExecutionOperation
    priority: int = DEFAULT_PRIORITY
    tags: tuple[str, ...] = EMPTY_TAGS
    metadata: ExecutionMetadata = field(default_factory=ExecutionMetadata)
    dependencies: tuple[ExecutionDependency, ...] = EMPTY_DEPENDENCIES
    constraints: tuple[ExecutionConstraint, ...] = EMPTY_CONSTRAINTS
    verifications: tuple[ExecutionVerification, ...] = EMPTY_VERIFICATIONS
    rollbacks: tuple[ExecutionRollback, ...] = EMPTY_ROLLBACKS

    def __hash__(self) -> int:
        return hash(self.step_id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExecutionStep):
            return NotImplemented
        return self.step_id == other.step_id  # type: ignore[no-any-return]

    def __lt__(self, other: "ExecutionStep") -> bool:
        if not isinstance(other, ExecutionStep):
            return NotImplemented
        return self.step_id < other.step_id  # type: ignore[no-any-return]
