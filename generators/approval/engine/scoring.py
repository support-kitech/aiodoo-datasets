"""Scoring logic for the Decision Engine."""

from typing import List, Tuple
from generators.approval.enums import DecisionEnum, ConfidenceLevel, Severity
from generators.approval.domain.finding import Finding


class DecisionScorer:
    """Calculates the decision and confidence based on findings."""

    @staticmethod
    def evaluate_decision(findings: List[Finding]) -> Tuple[DecisionEnum, ConfidenceLevel, str]:
        """Determine the final verdict and confidence score."""

        has_critical = any(f.severity == Severity.CRITICAL for f in findings if not f.is_positive)
        has_high = any(f.severity == Severity.HIGH for f in findings if not f.is_positive)
        has_medium = any(f.severity == Severity.MEDIUM for f in findings if not f.is_positive)

        if has_critical:
            decision = DecisionEnum.REJECTED
            reasoning = "Implementation contains critical flaws that violate core architecture or security principles."
        elif has_high or has_medium:
            decision = DecisionEnum.CHANGES_REQUESTED
            reasoning = "Implementation requires adjustments to meet style, performance, or Odoo conventions."
        else:
            decision = DecisionEnum.APPROVED
            reasoning = "Implementation meets all standard criteria."

        # Simplistic confidence scoring based on evidence volume vs severity
        confidence = ConfidenceLevel.HIGH if len(findings) > 0 else ConfidenceLevel.MEDIUM

        return decision, confidence, reasoning
