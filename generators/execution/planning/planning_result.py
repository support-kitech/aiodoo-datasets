"""Planning result."""

from dataclasses import dataclass, field
from generators.execution.planning.domain.execution_plan import PlannedExecution


@dataclass(frozen=True, slots=True)
class PlanningResult:
    """
    Immutable result from the Planning Engine.

    Attributes:
        success: Whether the planning was successful.
        planned_execution: The resulting PlannedExecution.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    planned_execution: PlannedExecution | None = None
    diagnostics: tuple[str, ...] = field(default_factory=tuple)
