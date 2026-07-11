"""Graph build result."""

from dataclasses import dataclass
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics


@dataclass(frozen=True, slots=True)
class GraphBuildResult:
    """Immutable result from GraphBuilder."""

    success: bool
    graph: ExecutionGraph
    diagnostics: BuilderDiagnostics
    statistics: GraphStatistics
