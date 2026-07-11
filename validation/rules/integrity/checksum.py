"""Rule: Manifest checksum must match the JSONL file."""

import hashlib
import json
from pathlib import Path

from validation.constants.framework import INTEGRITY_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class FileChecksumRule(BaseRule):
    """Manifest-declared checksum must match the actual JSONL file hash."""

    @property
    def rule_id(self) -> str:
        return "INT-004"

    @property
    def description(self) -> str:
        return "Manifest checksum must match the actual JSONL file."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.WARNING

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.INTEGRITY

    @property
    def priority(self) -> int:
        return INTEGRITY_RULE_PRIORITY + 3

    def validate(
        self, record: dict, context: ValidationContext  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        # This rule operates at the manifest level, not per-record.
        # It is invoked by ManifestValidator, not RecordValidator.
        return ()

    def validate_manifest(
        self, manifest_path: Path, dataset_dir: Path
    ) -> tuple[ValidationIssue, ...]:
        """Validate a manifest file's checksum against its JSONL file."""
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except (json.JSONDecodeError, OSError):
            return (
                ValidationIssue(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    category=self.category,
                    message=f"Cannot read manifest: {manifest_path.name}",
                    dataset_name=manifest_path.name,
                ),
            )

        declared_checksum = manifest.get("checksum", "")
        jsonl_filename = manifest.get("jsonl_filename", "")
        if not declared_checksum or not jsonl_filename:
            return ()

        jsonl_path = dataset_dir / jsonl_filename
        if not jsonl_path.exists():
            return (
                ValidationIssue(
                    rule_id=self.rule_id,
                    severity=ValidationSeverity.ERROR,
                    category=self.category,
                    message=f"JSONL file referenced in manifest not found: {jsonl_filename}",
                    dataset_name=manifest_path.name,
                ),
            )

        hasher = hashlib.sha256()
        with open(jsonl_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        actual_checksum = hasher.hexdigest()

        if actual_checksum != declared_checksum:
            return (
                ValidationIssue(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    category=self.category,
                    message=f"Checksum mismatch for {jsonl_filename}: expected={declared_checksum[:16]}... actual={actual_checksum[:16]}...",
                    dataset_name=manifest_path.name,
                ),
            )
        return ()
