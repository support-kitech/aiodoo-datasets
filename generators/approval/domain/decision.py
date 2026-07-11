"""Decision domain model."""

from dataclasses import dataclass
from generators.approval.enums import DecisionEnum, ConfidenceLevel


@dataclass(frozen=True, slots=True)
class Decision:
    """The final verdict containing the formulated reasoning and confidence score."""

    decision_id: str
    status: DecisionEnum
    confidence: ConfidenceLevel
    reasoning: str
