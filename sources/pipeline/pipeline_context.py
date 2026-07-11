"""Runtime context for the pipeline."""

from dataclasses import dataclass
from typing import Optional

from sources.domain.repository import ConfigurationSet
from sources.domain.context import RepositoryContext
from sources.cache.cache_key import CacheKey
from sources.cache.cache_metadata import CacheMetadata
from sources.pipeline.pipeline_options import PipelineOptions


@dataclass(slots=True)
class PipelineContext:
    """Mutable runtime state carrying data between pipeline stages."""

    options: PipelineOptions
    configuration_set: Optional[ConfigurationSet] = None
    repository_context: Optional[RepositoryContext] = None
    cache_key: Optional[CacheKey] = None
    cache_metadata: Optional[CacheMetadata] = None
