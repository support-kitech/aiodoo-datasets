"""Evidence domain model."""

from dataclasses import dataclass
from typing import Optional

from generators.approval.domain.source_generator import SourceGenerator


@dataclass(frozen=True, slots=True)
class Evidence:
    """Represents a verifiable piece of context for a review finding."""

    evidence_id: str
    source_generator: SourceGenerator  # e.g., 'planner', 'coding', 'execution', 'repair'
    source_reference: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    snippet: Optional[str] = None
    description: str = ""
