from dataclasses import dataclass
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.knowledge.execution_knowledge import (
    ExecutionKnowledge,
)
from generators.execution.statistics.builder_statistics import BuilderStatistics


@dataclass(frozen=True, slots=True)
class BuilderContext:
    """
    Immutable context passed to every Builder during the execution pipeline.
    It provides access to all upstream intelligence without allowing side-effects.
    """

    generator_version: str
    global_config: dict  # type: ignore[type-arg]
    analysis_context: AnalysisContext
    execution_knowledge: ExecutionKnowledge
    statistics: BuilderStatistics
