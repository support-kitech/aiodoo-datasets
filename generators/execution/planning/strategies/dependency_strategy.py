"""Dependency planning strategy."""

from generators.execution.planning.strategies.base_strategy import (
    BasePlanningStrategy,
)
from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.planning_result import PlanningResult


class DependencyStrategy(BasePlanningStrategy):  # type: ignore[misc]
    """Strategy that plans nodes based on their dependency graph."""

    def plan(self, context: PlanningContext) -> PlanningResult:
        # Placeholder for actual dependency strategy logic.
        return PlanningResult(success=True)
