"""Graph build result."""

from dataclasses import dataclass
from generators.execution.graph.graph import ExecutionGraph
from generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)
from generators.execution.graph.statistics import GraphStatistics


@dataclass(frozen=True, slots=True)
class GraphBuildResult:
    """Immutable result from GraphBuilder."""

    success: bool
    graph: ExecutionGraph
    diagnostics: BuilderDiagnostics
    statistics: GraphStatistics
