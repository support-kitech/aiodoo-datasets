"""Structural validator for ProtocolMetadata."""

from protocol.domain.metadata import ProtocolMetadata
from protocol.validation.base import ValidationResult


class MetadataValidator:
    """Validates structural integrity of ProtocolMetadata objects."""

    @staticmethod
    def validate(metadata: ProtocolMetadata) -> ValidationResult:
        errors: list[str] = []

        if not metadata.identifier.hash_value:
            errors.append("Metadata identifier hash_value is empty.")

        if metadata.properties is None:
            errors.append("Metadata properties must not be None.")

        return ValidationResult.failure(*errors) if errors else ValidationResult.success()
