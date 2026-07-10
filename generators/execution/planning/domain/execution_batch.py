"""Immutable representation of an execution batch."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.planning.domain.execution_phase import ExecutionPhase

@dataclass(frozen=True, slots=True)
class ExecutionBatch:
    """
    A specific batch of execution containing multiple phases.
    Batches are typically units of work that can be processed independently or sequentially.
    
    Attributes:
        batch_id: Unique identifier for the batch.
        is_parallel: Whether the phases in this batch can be executed in parallel.
        phases: Ordered tuple of execution phases in this batch.
    """
    batch_id: str
    is_parallel: bool
    phases: tuple[ExecutionPhase, ...] = field(default_factory=tuple)
    
    def __hash__(self) -> int:
        return hash(self.batch_id)
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExecutionBatch):
            return NotImplemented
        return self.batch_id == other.batch_id
