"""Immutable representation of an execution schedule."""

from dataclasses import dataclass, field
from generators.execution.planning.domain.execution_batch import ExecutionBatch


@dataclass(frozen=True, slots=True)
class ExecutionSchedule:
    """
    A specific schedule for execution containing multiple batches.

    Attributes:
        schedule_id: Unique identifier for the schedule.
        strategy: The strategy used to create the schedule.
        batches: Ordered tuple of execution batches in this schedule.
    """

    schedule_id: str
    strategy: str
    batches: tuple[ExecutionBatch, ...] = field(default_factory=tuple)

    def __hash__(self) -> int:
        return hash(self.schedule_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExecutionSchedule):
            return NotImplemented
        return self.schedule_id == other.schedule_id
