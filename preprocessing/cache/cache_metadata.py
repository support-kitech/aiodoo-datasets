"""CacheMetadata domain model."""

from dataclasses import dataclass
from typing import Mapping
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class CacheMetadata:
    """Immutable metadata tracking execution timing and cache entry properties."""
    
    cache_key: str
    created_at_iso: str
    framework_version: str
    python_version: str
    cache_schema_version: str
    serializer_version: str
    repository_context_hash: str
    preprocessed_context_hash: str
    processor_registry_hash: str
    statistics: Mapping[str, object] = MappingProxyType({})
