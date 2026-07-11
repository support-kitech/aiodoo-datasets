"""Master validation orchestrator for the Approval Generator."""

from typing import Tuple, Any
from generators.approval.domain.review import Review
from generators.approval.validation.review_validator import ReviewValidator
from generators.approval.exceptions import ApprovalValidationError


class ApprovalValidator:
    """Orchestrates all validation phases."""

    @staticmethod
    def validate_all(review: Review, _ignored: Any = None) -> Tuple[str, ...]:
        """Run all validators and return combined diagnostics. Fails fast on error."""
        diagnostics = []

        # 1. Review Validation
        try:
            review_diags = ReviewValidator.validate(review)
            diagnostics.extend(review_diags)
        except Exception as e:
            raise ApprovalValidationError(f"Review validation failed: {str(e)}") from e

        # Protocol and Dataset Validation Removed

        return tuple(diagnostics)
