"""Immutable representation of an execution phase."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.planning.domain.execution_stage import ExecutionStage


@dataclass(frozen=True, slots=True)
class ExecutionPhase:
    """
    A specific phase of execution containing multiple stages.

    Attributes:
        phase_id: Unique identifier for the phase.
        name: Human-readable name for the phase.
        stages: Ordered tuple of execution stages in this phase.
    """

    phase_id: str
    name: str
    stages: tuple[ExecutionStage, ...] = field(default_factory=tuple)

    def __hash__(self) -> int:
        return hash(self.phase_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExecutionPhase):
            return NotImplemented
        return self.phase_id == other.phase_id
