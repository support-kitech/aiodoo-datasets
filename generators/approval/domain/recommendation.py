"""Recommendation domain model."""

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class Recommendation:
    """Actionable steps linked to a negative finding."""
    recommendation_id: str
    finding_id: str
    description: str
    suggested_fix: Optional[str] = None
