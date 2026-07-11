"""Cache invalidation logic for the Sources Framework."""

import platform

from sources.cache.cache_key import CacheKey
from sources.cache.cache_metadata import CacheMetadata
from sources.cache.validation_result import CacheValidationResult, CacheValidationReason


class CacheInvalidator:
    """Validates if the existing cache is still valid."""

    @classmethod
    def get_python_version(cls) -> str:
        """Get the current Python version string."""
        return platform.python_version()

    @classmethod
    def validate(cls, key: CacheKey, metadata: CacheMetadata) -> CacheValidationResult:
        """
        Check if the cache metadata matches the current key and environment.

        Args:
            key: The expected cache key based on current configuration.
            metadata: The metadata loaded from the cache store.

        Returns:
            A CacheValidationResult indicating whether the cache is valid and why.
        """
        if metadata.cache_schema_version != key.cache_schema_version:
            return CacheValidationResult(False, CacheValidationReason.SCHEMA_CHANGED)

        if metadata.sources_framework_version != key.framework_version:
            return CacheValidationResult(False, CacheValidationReason.FRAMEWORK_CHANGED)

        if metadata.python_version != cls.get_python_version():
            return CacheValidationResult(False, CacheValidationReason.PYTHON_CHANGED)

        if metadata.configuration_hash != key.configuration_hash:
            return CacheValidationResult(False, CacheValidationReason.CONFIGURATION_CHANGED)
            
        if metadata.repository_hash != key.repository_hash:
            return CacheValidationResult(False, CacheValidationReason.REPOSITORY_CHANGED)

        return CacheValidationResult(True, CacheValidationReason.CACHE_HIT)
