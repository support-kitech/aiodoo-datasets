"""Parallel planning strategy."""

from generators.execution.planning.strategies.base_strategy import (
    BasePlanningStrategy,
)
from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.planning_result import PlanningResult


class ParallelStrategy(BasePlanningStrategy):  # type: ignore[misc]
    """Strategy that plans nodes to run in parallel where possible."""

    def plan(self, context: PlanningContext) -> PlanningResult:
        # Placeholder for actual parallel strategy logic.
        return PlanningResult(success=True)
