"""Structural validator for ProtocolSchema."""

from protocol.domain.schema import ProtocolSchema
from protocol.validation.base import ValidationResult


class SchemaValidator:
    """Validates structural integrity of ProtocolSchema objects."""

    @staticmethod
    def validate(schema: ProtocolSchema) -> ValidationResult:
        errors: list[str] = []

        if not schema.identifier.hash_value:
            errors.append("Schema identifier hash_value is empty.")

        if not schema.schema_version:
            errors.append("Schema version must not be empty.")

        return ValidationResult.failure(*errors) if errors else ValidationResult.success()
