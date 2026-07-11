"""Validates manifest JSON files against their referenced JSONL files."""

import logging

from validation.domain.enums import ValidationStatus
from validation.domain.models import ValidationContext
from validation.domain.results import ValidationResult
from validation.rules.integrity.checksum import FileChecksumRule

logger = logging.getLogger(__name__)


class ManifestValidator:
    """Validates manifest files by delegating to FileChecksumRule."""

    @staticmethod
    def validate(context: ValidationContext) -> ValidationResult:
        """Validate all manifest files in the dataset directory."""
        checksum_rule = FileChecksumRule()
        all_issues = []

        for manifest_path in context.manifest_files:
            if not manifest_path.exists():
                continue
            issues = checksum_rule.validate_manifest(manifest_path, context.dataset_dir)
            all_issues.extend(issues)

        status = ValidationStatus.FAILED if all_issues else ValidationStatus.PASSED
        return ValidationResult(
            status=status,
            issues=tuple(all_issues),
            dataset_name="manifests",
        )
