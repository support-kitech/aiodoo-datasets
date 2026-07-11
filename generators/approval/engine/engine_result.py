"""Engine result for the Approval Generator."""

from dataclasses import dataclass, field
from typing import Tuple
from generators.approval.domain.decision import Decision
from generators.approval.domain.finding import Finding
from generators.approval.domain.recommendation import Recommendation


@dataclass(frozen=True, slots=True)
class EngineResult:
    """The result of the Decision Engine evaluation."""

    success: bool
    decision: Decision
    findings: Tuple[Finding, ...] = field(default_factory=tuple)
    recommendations: Tuple[Recommendation, ...] = field(default_factory=tuple)
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)
