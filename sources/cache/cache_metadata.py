"""Domain models for cache metadata."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CacheMetadata:
    """Metadata describing the cache state. Safe to include timestamps here."""

    sources_framework_version: str
    cache_schema_version: str
    python_version: str
    repository_count: int
    module_count: int
    configuration_hash: str
    repository_hash: str
    creation_time: float
    last_validation: float
