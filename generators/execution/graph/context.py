"""Frozen context for all graph components."""

from dataclasses import dataclass, field
from typing import Any
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics


@dataclass(frozen=True, slots=True)
class GraphContext:
    """
    Immutable context passed to all Graph components.

    Contains upstream BuilderContext, domain objects from PipelineResult,
    statistics, and configuration. All graph components receive only GraphContext.
    """
    builder_context: BuilderContext
    domain_steps: tuple = field(default_factory=tuple)
    domain_dependencies: tuple = field(default_factory=tuple)
    statistics: GraphStatistics = field(default_factory=GraphStatistics)
    config: dict[str, Any] = field(default_factory=dict)
