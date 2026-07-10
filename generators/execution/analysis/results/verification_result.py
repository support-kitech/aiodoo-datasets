"""Verification result container."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.analysis.knowledge.verification_knowledge import VerificationKnowledge

@dataclass(frozen=True, eq=True)
class VerificationResult:
    """Result of verification analysis."""
    is_successful: bool
    verifications: tuple[VerificationKnowledge, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
