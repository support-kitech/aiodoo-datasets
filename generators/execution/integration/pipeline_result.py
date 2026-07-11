"""Immutable result for the Integration pipeline."""

from dataclasses import dataclass
from typing import Any
from generators.execution.builders.pipeline_result import (
    PipelineResult as BuildPipelineResult,
)
from generators.execution.graph.results.graph_build_result import GraphBuildResult
from generators.execution.planning.planning_result import PlanningResult
# removed ProtocolResult
from generators.execution.export.export_result import ExportResult
from generators.execution.integration.pipeline_statistics import PipelineStatistics


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """
    Result of the end-to-end integration pipeline.

    Attributes:
        success: Whether the pipeline completed successfully.
        analysis_result: Result from the Analysis phase.
        build_result: Result from the Builders phase.
        graph_result: Result from the Graph phase.
        planning_result: Result from the Planning phase.
        protocol_result: Result from the Protocol phase.
        export_result: Result from the Export phase.
        statistics: The final state of PipelineStatistics.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    analysis_result: Any | None = None
    build_result: BuildPipelineResult | None = None
    graph_result: GraphBuildResult | None = None
    planning_result: PlanningResult | None = None
    protocol_result: Any | None = None
    export_result: ExportResult | None = None
    statistics: PipelineStatistics | None = None
    diagnostics: tuple[str, ...] = tuple()
    
    @property
    def status(self) -> "Any":
        from generators.common.pipeline.status import PipelineStatus
        if not self.success and any(d == "Graph contains no nodes." for d in self.diagnostics):
            return PipelineStatus.SKIPPED
        return PipelineStatus.SUCCESS if self.success else PipelineStatus.FAILED
