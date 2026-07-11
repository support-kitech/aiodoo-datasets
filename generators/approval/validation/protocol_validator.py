"""Protocol validator for the Approval Generator."""

from typing import Tuple
from aiodoo_datasets.generators.approval.protocol.domain.approval_protocol import ApprovalProtocol
from aiodoo_datasets.generators.approval.exceptions import ValidationException


class ProtocolValidator:
    """Validates the serializable ApprovalProtocol structure."""

    @staticmethod
    def validate(protocol: ApprovalProtocol) -> Tuple[str, ...]:
        """Ensure the mapped ApprovalProtocol matches schema specs."""
        diagnostics = []

        if not protocol.metadata.generator_version:
            diagnostics.append("Missing generator_version in Protocol metadata.")

        if not protocol.decision.status:
            diagnostics.append("Missing decision status in Protocol.")

        if diagnostics:
            raise ValidationException(f"Protocol validation failed: {diagnostics}")

        return tuple(diagnostics)
