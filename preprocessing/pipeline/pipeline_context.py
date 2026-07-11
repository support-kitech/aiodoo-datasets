"""PipelineContext for the PreprocessingPipeline."""

from dataclasses import dataclass
from typing import Optional

from sources.domain.context import RepositoryContext
from preprocessing.pipeline.pipeline_options import PipelineOptions
from preprocessing.cache.cache_key import CacheKey


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """Immutable state passed sequentially through the Pipeline execution."""
    
    source_context: RepositoryContext
    options: PipelineOptions
    cache_key: Optional[CacheKey] = None
    
    def with_update(self, **kwargs) -> "PipelineContext":
        """Return a new immutable instance with updated fields."""
        from dataclasses import replace
        return replace(self, **kwargs)
