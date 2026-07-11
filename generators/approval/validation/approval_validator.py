"""Master validation orchestrator for the Approval Generator."""

from typing import Tuple
from generators.approval.domain.review import Review
from generators.approval.protocol.domain.approval_protocol import ApprovalProtocol
from generators.approval.validation.review_validator import ReviewValidator
from generators.approval.validation.protocol_validator import ProtocolValidator
from generators.approval.validation.dataset_validator import DatasetValidator
from generators.approval.exceptions import ApprovalValidationError


class ApprovalValidator:
    """Orchestrates all validation phases."""

    @staticmethod
    def validate_all(review: Review, protocol: ApprovalProtocol) -> Tuple[str, ...]:
        """Run all validators and return combined diagnostics. Fails fast on error."""
        diagnostics = []

        # 1. Review Validation
        try:
            review_diags = ReviewValidator.validate(review)
            diagnostics.extend(review_diags)
        except Exception as e:
            raise ApprovalValidationError(f"Review validation failed: {str(e)}") from e

        # 2. Protocol Validation
        try:
            proto_diags = ProtocolValidator.validate(protocol)
            diagnostics.extend(proto_diags)
        except Exception as e:
            raise ApprovalValidationError(f"Protocol validation failed: {str(e)}") from e

        # 3. Dataset Validation
        try:
            dataset_diags = DatasetValidator.validate([protocol])
            diagnostics.extend(dataset_diags)
        except Exception as e:
            raise ApprovalValidationError(f"Dataset validation failed: {str(e)}") from e

        return tuple(diagnostics)
