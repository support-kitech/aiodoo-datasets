"""Category domain model for Evaluation Generator."""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Category:
    """Immutable evaluation category."""
    category_id: str
    name: str
    description: str
