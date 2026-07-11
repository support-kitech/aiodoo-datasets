"""Observational metrics for the Validation Framework."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationMetrics:
    """Timing and counter metrics for a validation execution. Never influences flow."""

    rule_execution_ms: float = 0.0
    io_ms: float = 0.0
    aggregation_ms: float = 0.0
    total_ms: float = 0.0
    rules_executed: int = 0
    rules_skipped: int = 0
