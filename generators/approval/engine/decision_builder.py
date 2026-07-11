"""Decision builder for the Approval Generator."""

import hashlib
from typing import Tuple
from generators.approval.domain.decision import Decision
from generators.approval.enums import DecisionEnum, ConfidenceLevel
from generators.approval.domain.finding import Finding


class DecisionBuilder:
    """Builds the final immutable Decision object."""

    @staticmethod
    def build(
        status: DecisionEnum,
        confidence: ConfidenceLevel,
        reasoning: str,
        findings: Tuple[Finding, ...],
    ) -> Decision:
        """Construct a fully formed immutable Decision."""

        # Create deterministic input string
        finding_ids = ",".join(sorted(f.finding_id for f in findings))
        base_string = f"{status.value}:{confidence.value}:{finding_ids}"

        # Generate deterministic ID
        deterministic_hash = hashlib.sha256(base_string.encode("utf-8")).hexdigest()[:8]

        return Decision(
            decision_id=f"DEC-{deterministic_hash}",
            status=status,
            confidence=confidence,
            reasoning=reasoning,
        )
