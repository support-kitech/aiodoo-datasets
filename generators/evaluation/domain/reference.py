"""Reference domain model for Evaluation Generator."""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Reference:
    """Immutable pointer to a source protocol."""
    source_generator: str
    source_reference: str
    description: str
