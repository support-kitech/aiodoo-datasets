"""Structural validator for ProtocolDataset."""

from protocol.domain.dataset import ProtocolDataset
from protocol.validation.base import ValidationResult
from protocol.validation.manifest_validator import ManifestValidator
from protocol.validation.schema_validator import SchemaValidator


class DatasetValidator:
    """Validates structural integrity of ProtocolDataset objects."""

    @staticmethod
    def validate(dataset: ProtocolDataset) -> ValidationResult:
        errors: list[str] = []

        if not dataset.identifier.hash_value:
            errors.append("Dataset identifier hash_value is empty.")

        # Validate nested manifest.
        manifest_result = ManifestValidator.validate(dataset.manifest)
        if not manifest_result.valid:
            errors.extend(f"Manifest: {e}" for e in manifest_result.errors)

        # Validate nested schema.
        schema_result = SchemaValidator.validate(dataset.schema)
        if not schema_result.valid:
            errors.extend(f"Schema: {e}" for e in schema_result.errors)

        return ValidationResult.failure(*errors) if errors else ValidationResult.success()
