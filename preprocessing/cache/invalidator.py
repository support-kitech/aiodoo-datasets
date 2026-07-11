"""Cache invalidator."""

from preprocessing.constants.framework import PREPROCESSING_FRAMEWORK_VERSION
from preprocessing.cache.cache_metadata import CacheMetadata
from preprocessing.cache.validation_result import CacheValidationResult


class CacheInvalidator:
    """Validates if a cached payload is still valid for the current framework state."""
    
    @staticmethod
    def validate(metadata: CacheMetadata | None) -> CacheValidationResult:
        if not metadata:
            return CacheValidationResult(
                is_valid=False,
                reason="Cache metadata missing.",
                requires_full_rebuild=True
            )
            
        if metadata.framework_version != PREPROCESSING_FRAMEWORK_VERSION:
            return CacheValidationResult(
                is_valid=False,
                reason=f"Framework version mismatch. Cache: {metadata.framework_version}, Current: {PREPROCESSING_FRAMEWORK_VERSION}",
                requires_full_rebuild=True
            )
            
        return CacheValidationResult(is_valid=True, reason="Valid.", requires_full_rebuild=False)
