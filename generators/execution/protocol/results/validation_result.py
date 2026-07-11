"""Validation result objects."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Immutable result from ProtocolValidator.

    Attributes:
        success: Whether validation was successful.
        violations: List of validation failures.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    violations: tuple[str, ...] = tuple()
    diagnostics: tuple[str, ...] = tuple()
