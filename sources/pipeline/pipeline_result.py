"""Execution results returned by the pipeline."""

from dataclasses import dataclass
from typing import Optional

from sources.domain.context import RepositoryContext
from sources.cache.validation_result import CacheValidationResult
from sources.pipeline.pipeline_statistics import PipelineStatistics


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Immutable result representing the entire pipeline execution."""

    success: bool
    context: Optional[RepositoryContext]
    cache_validation: Optional[CacheValidationResult]
    statistics: PipelineStatistics
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
