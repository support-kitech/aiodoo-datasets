"""Dependency planning strategy."""

from aiodoo_datasets.generators.execution.planning.strategies.base_strategy import BasePlanningStrategy
from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult

class DependencyStrategy(BasePlanningStrategy):
    """Strategy that plans nodes based on their dependency graph."""
    
    def plan(self, context: PlanningContext) -> PlanningResult:
        # Placeholder for actual dependency strategy logic.
        return PlanningResult(success=True)
