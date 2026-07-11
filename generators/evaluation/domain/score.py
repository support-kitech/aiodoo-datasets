"""Evaluation Score domain model for Evaluation Generator."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationScore:
    """Immutable score components."""

    score_id: str
    metric_name: str
    raw_score: float
    max_score: float
    normalized_score: float
    weight: float
    pass_threshold: float
    result: bool
