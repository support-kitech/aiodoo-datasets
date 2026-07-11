"""Enum and dataclass for cache validation results."""

from enum import Enum
from dataclasses import dataclass


class CacheValidationReason(Enum):
    """Reasons for cache validation outcomes."""

    CACHE_HIT = "CACHE_HIT"
    CACHE_MISSING = "CACHE_MISSING"
    SCHEMA_CHANGED = "SCHEMA_CHANGED"
    FRAMEWORK_CHANGED = "FRAMEWORK_CHANGED"
    PYTHON_CHANGED = "PYTHON_CHANGED"
    CONFIGURATION_CHANGED = "CONFIGURATION_CHANGED"
    REPOSITORY_CHANGED = "REPOSITORY_CHANGED"
    CORRUPTED_CACHE = "CORRUPTED_CACHE"


@dataclass(frozen=True, slots=True)
class CacheValidationResult:
    """The outcome of cache validation."""

    is_valid: bool
    reason: CacheValidationReason
