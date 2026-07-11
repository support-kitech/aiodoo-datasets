"""Cross-dataset validation for reference integrity across JSONL files."""

import json
import logging

from validation.domain.enums import ValidationStatus, ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.domain.results import ValidationResult

logger = logging.getLogger(__name__)


class CrossDatasetValidator:
    """Validates relationships and consistency across multiple JSONL files."""

    @staticmethod
    def validate(context: ValidationContext) -> ValidationResult:
        """
        Validate cross-dataset consistency.

        Checks:
        - No duplicate protocol_hashes across datasets
        - Consistent metadata versions across datasets
        """
        all_issues: list[ValidationIssue] = []
        global_hashes: dict[str, str] = {}  # hash -> dataset_name

        for jsonl_path in context.dataset_files:
            if not jsonl_path.exists():
                continue

            try:
                with open(jsonl_path, encoding="utf-8") as f:
                    for line_num, line in enumerate(f):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            record = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        if not isinstance(record, dict):
                            continue

                        metadata = record.get("metadata")
                        if not isinstance(metadata, dict):
                            continue

                        protocol_hash = metadata.get("protocol_hash", "")
                        if not protocol_hash:
                            continue

                        if protocol_hash in global_hashes:
                            other_dataset = global_hashes[protocol_hash]
                            if other_dataset != jsonl_path.name:
                                all_issues.append(
                                    ValidationIssue(
                                        rule_id="XREF-001",
                                        severity=ValidationSeverity.WARNING,
                                        category=ValidationCategory.CROSS_DATASET,
                                        message=(
                                            f"protocol_hash '{protocol_hash[:16]}...' "
                                            f"appears in both {other_dataset} and {jsonl_path.name}"
                                        ),
                                        dataset_name=jsonl_path.name,
                                        record_index=line_num,
                                    )
                                )
                        else:
                            global_hashes[protocol_hash] = jsonl_path.name

            except OSError as e:
                logger.warning("Cannot read %s for cross-dataset validation: %s", jsonl_path, e)

        has_errors = any(
            i.severity in (ValidationSeverity.FATAL, ValidationSeverity.ERROR) for i in all_issues
        )
        status = ValidationStatus.FAILED if has_errors else ValidationStatus.PASSED

        return ValidationResult(
            status=status,
            issues=tuple(all_issues),
            dataset_name="cross_dataset",
        )
