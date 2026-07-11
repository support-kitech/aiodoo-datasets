"""CacheKey domain model."""

from dataclasses import dataclass
import hashlib

from preprocessing.constants.framework import PREPROCESSING_FRAMEWORK_VERSION


@dataclass(frozen=True, slots=True)
class CacheKey:
    """
    Immutable representation of a cache key.
    Combines the Source RepositoryContext hash with the Preprocessing framework version.
    """

    source_context_hash: str
    framework_version: str = PREPROCESSING_FRAMEWORK_VERSION

    @property
    def value(self) -> str:
        """Deterministic cache key string."""
        raw_key = f"{self.source_context_hash}_{self.framework_version}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
