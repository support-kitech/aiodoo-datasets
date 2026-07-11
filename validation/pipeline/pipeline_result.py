"""Immutable pipeline result for the Validation Framework."""

from dataclasses import dataclass

from validation.domain.results import ValidationReport
from validation.pipeline.pipeline_statistics import PipelineStatistics


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Immutable result of the validation pipeline execution."""

    success: bool
    report: ValidationReport
    statistics: PipelineStatistics
    error_message: str | None = None
