"""Decision validator for the Approval Generator."""

from typing import Tuple
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.enums import DecisionEnum, Severity
from aiodoo_datasets.generators.approval.exceptions import ValidationException

class DecisionValidator:
    """Validates the logic behind a Decision."""
    
    @staticmethod
    def validate(review: Review) -> Tuple[str, ...]:
        """Ensure APPROVED states contain no CRITICAL severity findings."""
        diagnostics = []
        
        if review.decision.status == DecisionEnum.APPROVED:
            critical_findings = [f for f in review.findings if f.severity == Severity.CRITICAL and not f.is_positive]
            if critical_findings:
                diagnostics.append(f"Review is APPROVED but contains {len(critical_findings)} CRITICAL findings.")
                
        if not review.decision.reasoning:
            diagnostics.append("Decision is missing required reasoning.")
            
        if diagnostics:
            raise ValidationException(f"Decision validation failed: {diagnostics}")
            
        return tuple(diagnostics)
