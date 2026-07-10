"""Context passed to rules during evaluation."""

from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata

@dataclass(frozen=True, slots=True)
class RuleContext:
    """Context passed to rules during evaluation."""
    evidence_pool: Tuple[Evidence, ...]
    metadata: ReviewMetadata
    config: Any = None  # Generic Any to avoid circular config dependencies early on
    statistics: Dict[str, Any] = field(default_factory=dict)
