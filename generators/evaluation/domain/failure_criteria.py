"""Failure Criteria domain model for Evaluation Generator."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FailureCriteria:
    """Immutable failure criteria for evaluation."""

    criteria_id: str
    description: str
    fatal: bool
