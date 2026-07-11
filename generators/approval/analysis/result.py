"""Analysis result for the Approval Generator."""

from dataclasses import dataclass, field
from typing import Tuple
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """The result of ingesting and extracting evidence from upstream protocols."""

    success: bool
    metadata: ReviewMetadata
    evidence_pool: Tuple[Evidence, ...] = field(default_factory=tuple)
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)
