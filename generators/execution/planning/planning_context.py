"""Immutable context for the Planning Engine."""

from dataclasses import dataclass
from typing import Any
from types import MappingProxyType
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics
from aiodoo_datasets.generators.execution.planning.enums import PlanningStrategyType
from aiodoo_datasets.generators.execution.planning.planning_statistics import PlanningStatistics


@dataclass(frozen=True, slots=True)
class PlanningContext:
    """
    Context carrying strictly necessary data for planning.
    Completely isolated from upstream Analysis and Builder contexts.

    Attributes:
        graph: The validated ExecutionGraph to be planned.
        graph_statistics: Statistics of the incoming graph.
        configuration: Global configuration limits and rules.
        strategy: The active planning strategy type to employ.
        planning_statistics: Mutable statistics container for the planning phase.
    """

    graph: ExecutionGraph
    graph_statistics: GraphStatistics
    configuration: MappingProxyType[str, Any]
    strategy: PlanningStrategyType
    planning_statistics: PlanningStatistics
