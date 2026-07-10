"""Immutable representation of the final execution plan from the Planning Engine."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.planning.domain.execution_schedule import ExecutionSchedule

@dataclass(frozen=True, slots=True)
class PlannedExecution:
    """
    The fully planned execution sequence resulting from the Planning Engine.
    Named PlannedExecution to avoid collision with Phase 1 ExecutionPlan if imported together,
    though it resides in planning/domain/execution_plan.py per specification.
    
    Attributes:
        plan_id: Unique deterministic identifier for the plan.
        graph_id: The ID of the ExecutionGraph this plan was built from.
        schedules: Ordered tuple of execution schedules.
    """
    plan_id: str
    graph_id: str
    schedules: tuple[ExecutionSchedule, ...] = field(default_factory=tuple)
    
    def __hash__(self) -> int:
        return hash(self.plan_id)
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlannedExecution):
            return NotImplemented
        return self.plan_id == other.plan_id
