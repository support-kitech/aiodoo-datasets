"""Immutable context for the Protocol Mapping pipeline."""

from dataclasses import dataclass
from typing import Any
from types import MappingProxyType
from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult
from aiodoo_datasets.generators.execution.planning.planning_statistics import PlanningStatistics
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics


@dataclass(frozen=True, slots=True)
class ProtocolContext:
    """
    Context carrying only necessary data for protocol mapping.

    Attributes:
        planning_result: The result of the planning phase.
        planning_statistics: Statistics from the planning phase.
        configuration: Global configuration limits and rules.
        protocol_version: The version string for the protocol schema.
        protocol_statistics: Mutable statistics container for the protocol phase.
    """

    planning_result: PlanningResult
    planning_statistics: PlanningStatistics
    configuration: MappingProxyType[str, Any]
    protocol_version: str
    protocol_statistics: ProtocolStatistics
