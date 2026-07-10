from dataclasses import dataclass, field
from types import MappingProxyType
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.builders.diagnostics.builder_diagnostics import BuilderDiagnostics
from aiodoo_datasets.generators.execution.statistics.builder_statistics import BuilderStatistics

@dataclass(frozen=True, slots=True)
class PipelineResult:
    """
    Immutable final output aggregating all Builder node results, statistics, and anomalies.
    """
    success: bool
    results: MappingProxyType[str, BaseBuildResult]
    diagnostics: BuilderDiagnostics
    statistics: BuilderStatistics
    failed_builders: tuple[str, ...] = field(default_factory=tuple)
    skipped_builders: tuple[str, ...] = field(default_factory=tuple)
