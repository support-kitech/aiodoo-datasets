"""PipelineResult domain model."""

from dataclasses import dataclass
from typing import Optional

from preprocessing.domain.context import PreprocessedRepositoryContext
from preprocessing.pipeline.pipeline_statistics import PipelineStatistics


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Immutable result of a PreprocessingPipeline execution."""
    
    success: bool
    context: Optional[PreprocessedRepositoryContext]
    statistics: PipelineStatistics
    error_message: Optional[str] = None
