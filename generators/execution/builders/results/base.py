from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)
from aiodoo_datasets.generators.execution.statistics.builder_statistics import BuilderStatistics


@dataclass(frozen=True, slots=True)
class BaseBuildResult:
    """Base class for all Builder returns."""

    builder_name: str
    builder_version: str
    execution_time: float
    success: bool
    diagnostics: BuilderDiagnostics
    statistics: BuilderStatistics
