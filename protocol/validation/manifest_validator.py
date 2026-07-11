"""Structural validator for ProtocolManifest."""

from protocol.domain.manifest import ProtocolManifest
from protocol.validation.base import ValidationResult
from protocol.validation.metadata_validator import MetadataValidator
from protocol.validation.reference_validator import ReferenceValidator


class ManifestValidator:
    """Validates structural integrity of ProtocolManifest objects."""

    @staticmethod
    def validate(manifest: ProtocolManifest) -> ValidationResult:
        errors: list[str] = []

        if not manifest.identifier.hash_value:
            errors.append("Manifest identifier hash_value is empty.")

        # Validate nested metadata.
        meta_result = MetadataValidator.validate(manifest.metadata)
        if not meta_result.valid:
            errors.extend(f"Metadata: {e}" for e in meta_result.errors)

        # Validate nested repository reference.
        ref_result = ReferenceValidator.validate(manifest.repository_reference)
        if not ref_result.valid:
            errors.extend(f"RepositoryRef: {e}" for e in ref_result.errors)

        # Validate version fields.
        if not manifest.version.framework_version:
            errors.append("Manifest version.framework_version must not be empty.")

        if not manifest.version.schema_version:
            errors.append("Manifest version.schema_version must not be empty.")

        return ValidationResult.failure(*errors) if errors else ValidationResult.success()
