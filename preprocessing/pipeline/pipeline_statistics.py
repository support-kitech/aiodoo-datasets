"""PipelineStatistics domain model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineStatistics:
    """
    Observational statistics for the entire pipeline execution.
    Never influences execution flow.
    """
    
    validation_time: float = 0.0
    cache_lookup_time: float = 0.0
    processing_time: float = 0.0
    builder_time: float = 0.0
    serialization_time: float = 0.0
    deserialization_time: float = 0.0
    cache_write_time: float = 0.0
    total_duration: float = 0.0
    cache_hit: bool = False
    cache_miss: bool = False
    files_processed: int = 0
    repositories_processed: int = 0
