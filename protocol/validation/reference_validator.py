"""Structural validator for ProtocolReference."""

from protocol.domain.references import ProtocolReference
from protocol.validation.base import ValidationResult


class ReferenceValidator:
    """Validates structural integrity of ProtocolReference objects."""

    @staticmethod
    def validate(reference: ProtocolReference) -> ValidationResult:
        errors: list[str] = []

        if not reference.identifier.hash_value:
            errors.append("Reference identifier hash_value is empty.")

        if not reference.target_identifier:
            errors.append("Reference target_identifier must not be empty.")

        return ValidationResult.failure(*errors) if errors else ValidationResult.success()
