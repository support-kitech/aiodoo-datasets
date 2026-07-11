"""Base validation models for the Protocol Framework."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Immutable result of a structural validation check.

    Validation never mutates, repairs, or normalizes.
    It only reports whether the object is structurally valid.

    Designed to be reusable by the future Validation Framework.
    """

    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    statistics: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    summary: str = ""

    @staticmethod
    def success(*, summary: str = "") -> "ValidationResult":
        """Create a passing validation result."""
        return ValidationResult(valid=True, summary=summary)

    @staticmethod
    def failure(
        *errors: str, warnings: tuple[str, ...] = (), summary: str = ""
    ) -> "ValidationResult":
        """Create a failing validation result with error messages."""
        return ValidationResult(valid=False, errors=errors, warnings=warnings, summary=summary)

    def merge(self, other: "ValidationResult") -> "ValidationResult":
        """Combine two results. Invalid if either is invalid."""
        merged_stats = dict(self.statistics)
        merged_stats.update(other.statistics)
        return ValidationResult(
            valid=self.valid and other.valid,
            errors=self.errors + other.errors,
            warnings=self.warnings + other.warnings,
            statistics=MappingProxyType(merged_stats),
            summary=self.summary or other.summary,
        )
