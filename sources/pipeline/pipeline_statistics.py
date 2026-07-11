"""Runtime execution statistics for the Sources Framework pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineStatistics:
    """Immutable runtime statistics tracking execution details."""

    repositories_loaded: int = 0
    repositories_scanned: int = 0
    modules_discovered: int = 0
    modules_loaded: int = 0
    cache_hit: bool = False
    cache_miss: bool = False
    scan_duration: float = 0.0
    cache_duration: float = 0.0
    total_duration: float = 0.0
    warnings: int = 0
    errors: int = 0
