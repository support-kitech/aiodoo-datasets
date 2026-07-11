"""Dataset validator for the Approval Generator."""

from typing import Tuple, List
from aiodoo_datasets.generators.approval.protocol.domain.approval_protocol import ApprovalProtocol
from aiodoo_datasets.generators.approval.exceptions import ValidationException


class DatasetValidator:
    """Validates the entire exported dataset."""

    @staticmethod
    def validate(dataset: List[ApprovalProtocol]) -> Tuple[str, ...]:
        """Ensure no global anomalies exist in the dataset."""
        diagnostics = []

        if not dataset:
            diagnostics.append("Dataset is empty.")

        # Example validation: ensure unique IDs
        ids = set()
        for protocol in dataset:
            if protocol.review_id in ids:
                diagnostics.append(f"Duplicate protocol ID found: {protocol.review_id}")
            ids.add(protocol.review_id)

        if diagnostics:
            raise ValidationException(f"Dataset validation failed: {diagnostics}")

        return tuple(diagnostics)
