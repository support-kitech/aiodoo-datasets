"""Immutable representation of an entire execution workflow."""

from dataclasses import dataclass, field
from typing import Any
from types import MappingProxyType
from generators.execution.domain.execution_step import ExecutionStep
from generators.execution.environment.environment import ExecutionEnvironment
from generators.execution.domain.execution_metadata import ExecutionMetadata
from generators.execution.domain.types import PlanId


@dataclass(frozen=True)
class ExecutionPlan:
    """
    The final, topologically sorted sequence of execution steps.

    Attributes:
        plan_id: Unique deterministic SHA-256 identifier for the full workflow.
        environment: The contextual deployment limits.
        steps: Topologically ordered tuple of execution steps.
        metadata: Workflow metadata excluded from hashing.
        statistics: Immutable mapping for dataset metrics.
    """

    plan_id: PlanId
    environment: ExecutionEnvironment
    steps: tuple[ExecutionStep, ...] = field(default_factory=tuple)
    metadata: ExecutionMetadata = field(default_factory=ExecutionMetadata)
    statistics: MappingProxyType[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __hash__(self) -> int:
        return hash(self.plan_id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExecutionPlan):
            return NotImplemented
        return self.plan_id == other.plan_id  # type: ignore[no-any-return]
