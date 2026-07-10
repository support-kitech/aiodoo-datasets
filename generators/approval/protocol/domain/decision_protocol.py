"""Decision protocol model."""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DecisionProtocol:
    """Serializable decision structure."""
    decision_id: str
    status: str
    confidence: str
    reasoning: str
