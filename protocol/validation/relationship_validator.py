"""Structural validator for ProtocolRelationship."""

from protocol.domain.relationships import ProtocolRelationship
from protocol.validation.base import ValidationResult
from protocol.validation.reference_validator import ReferenceValidator


class RelationshipValidator:
    """Validates structural integrity of ProtocolRelationship objects."""

    @staticmethod
    def validate(relationship: ProtocolRelationship) -> ValidationResult:
        errors: list[str] = []

        if not relationship.identifier.hash_value:
            errors.append("Relationship identifier hash_value is empty.")

        # Validate that source and target references are themselves valid.
        src_result = ReferenceValidator.validate(relationship.source)
        tgt_result = ReferenceValidator.validate(relationship.target)

        if not src_result.valid:
            errors.extend(f"Source: {e}" for e in src_result.errors)

        if not tgt_result.valid:
            errors.extend(f"Target: {e}" for e in tgt_result.errors)

        # Source and target must not be the same reference.
        if relationship.source.identifier == relationship.target.identifier:
            errors.append("Relationship source and target must not be identical.")

        return ValidationResult.failure(*errors) if errors else ValidationResult.success()
