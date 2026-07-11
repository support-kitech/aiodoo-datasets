"""Success Criteria domain model for Evaluation Generator."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SuccessCriteria:
    """Immutable success criteria for evaluation."""

    criteria_id: str
    description: str
    weight: float
