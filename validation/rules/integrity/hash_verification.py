"""Rule: Protocol hash must be a valid SHA-256 hex string."""

import re

from validation.constants.framework import INTEGRITY_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")


class HashVerificationRule(BaseRule):
    """protocol_hash must be a valid 64-character hex SHA-256 digest."""

    @property
    def rule_id(self) -> str:
        return "INT-001"

    @property
    def description(self) -> str:
        return "protocol_hash must be a valid SHA-256 hex string."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.FATAL

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.INTEGRITY

    @property
    def priority(self) -> int:
        return INTEGRITY_RULE_PRIORITY

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        metadata = record.get("metadata")
        if not isinstance(metadata, dict):
            return ()

        protocol_hash = metadata.get("protocol_hash")
        if protocol_hash is None:
            return ()  # META-001 handles missing fields

        if not isinstance(protocol_hash, str) or not SHA256_PATTERN.match(protocol_hash):
            return (
                self._issue(
                    message=f"Invalid protocol_hash format: '{protocol_hash}'",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="metadata.protocol_hash",
                ),
            )
        return ()
