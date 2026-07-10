"""Schedule build result."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.planning.domain.execution_schedule import ExecutionSchedule

@dataclass(frozen=True, slots=True)
class ScheduleResult:
    """
    Immutable result from ScheduleBuilder.
    
    Attributes:
        success: Whether the schedule generation was successful.
        schedules: Ordered tuple of generated schedules.
        diagnostics: Any diagnostic messages.
    """
    success: bool
    schedules: tuple[ExecutionSchedule, ...] = field(default_factory=tuple)
    diagnostics: tuple[str, ...] = field(default_factory=tuple)
