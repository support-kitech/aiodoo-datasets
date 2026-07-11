"""Evaluation Rule domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class EvaluationRule:
    """Immutable evaluation rule representing a deterministic check."""

    rule_id: str
    description: str
    rule_type: str
    parameters: Tuple[str, ...]
