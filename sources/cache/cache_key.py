"""Domain models for deterministic cache keys."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CacheKey:
    """Immutable cache key representing a deterministic repository state."""

    repository_name: str
    configuration_hash: str
    repository_hash: str
    framework_version: str
    python_version: str
    cache_schema_version: str
