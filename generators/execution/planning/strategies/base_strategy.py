"""Base interface for planning strategies."""

import abc
from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult

class BasePlanningStrategy(abc.ABC):
    """Abstract base class for planning strategies."""
    
    @abc.abstractmethod
    def plan(self, context: PlanningContext) -> PlanningResult:
        """Execute the planning strategy to produce a PlanningResult."""
        pass
