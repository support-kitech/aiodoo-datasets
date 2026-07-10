"""Review validator for the Approval Generator."""

from typing import Tuple
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.exceptions import ValidationException

class ReviewValidator:
    """Validates structural integrity of a Review."""
    
    @staticmethod
    def validate(review: Review) -> Tuple[str, ...]:
        """Ensure findings and recommendations map correctly."""
        diagnostics = []
        
        finding_ids = {f.finding_id for f in review.findings}
        for rec in review.recommendations:
            if rec.finding_id not in finding_ids:
                diagnostics.append(f"Recommendation {rec.recommendation_id} references missing finding {rec.finding_id}")
                
        if diagnostics:
            raise ValidationException(f"Review validation failed: {diagnostics}")
            
        return tuple(diagnostics)
