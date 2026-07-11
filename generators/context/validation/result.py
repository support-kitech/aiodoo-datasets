"""Validation Result object."""

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Standardized result object for all validators."""

    valid: bool
    validator: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
