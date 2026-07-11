"""Cache validation result model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CacheValidationResult:
    """Immutable result of a cache validation check."""

    is_valid: bool
    reason: str
    requires_full_rebuild: bool
