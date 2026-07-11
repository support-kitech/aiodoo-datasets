"""Sequential planning strategy."""

from aiodoo_datasets.generators.execution.planning.strategies.base_strategy import (
    BasePlanningStrategy,
)
from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult


class SequentialStrategy(BasePlanningStrategy):  # type: ignore[misc]
    """Strategy that plans nodes sequentially."""

    def plan(self, context: PlanningContext) -> PlanningResult:
        # Strategy logic delegates to the planner to use builders sequentially.
        # This is a placeholder for actual strategy logic.
        return PlanningResult(success=True)
