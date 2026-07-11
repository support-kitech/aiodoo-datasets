"""Validation result."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Immutable result from graph validation."""

    success: bool
    violations: tuple[str, ...] = field(default_factory=tuple)
