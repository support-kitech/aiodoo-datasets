"""Validates an entire JSONL dataset file by streaming records."""

import json
import logging
import time
from pathlib import Path

from validation.domain.enums import ValidationStatus, ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.domain.results import ValidationResult
from validation.rules.base import BaseRule
from validation.schemas.base import DatasetSchema
from validation.validators.record_validator import RecordValidator

logger = logging.getLogger(__name__)


class DatasetValidator:
    """
    Validates an entire JSONL file.

    Streams line-by-line for memory efficiency.
    Manages lifecycle of stateful rules (e.g., DuplicateDetectionRule).
    """

    @staticmethod
    def validate(
        jsonl_path: Path,
        rules: tuple[BaseRule, ...],
        context: ValidationContext,
        max_issues: int = 1000,
        schema: DatasetSchema | None = None,
    ) -> ValidationResult:
        """
        Validate all records in a JSONL file.

        Args:
            jsonl_path: Path to the JSONL file.
            rules: Sorted tuple of rules to apply.
            context: Immutable validation context.
            max_issues: Cap on total issues to prevent OOM.
            schema: Resolved schema for this dataset's generator.

        Returns:
            ValidationResult for the entire dataset.
        """
        start = time.perf_counter()
        dataset_name = jsonl_path.name
        all_issues: list[ValidationIssue] = []
        records_validated = 0

        # Reset stateful rules
        for rule in rules:
            reset = getattr(rule, "reset", None)
            if callable(reset):
                reset()

        if not jsonl_path.exists():
            return ValidationResult.failure(
                ValidationIssue(
                    rule_id="SER-001",
                    severity=ValidationSeverity.FATAL,
                    category=ValidationCategory.SERIALIZATION,
                    message=f"Dataset file not found: {dataset_name}",
                    dataset_name=dataset_name,
                ),
                dataset_name=dataset_name,
            )

        with open(jsonl_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue

                # JSON parse check
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as e:
                    all_issues.append(
                        ValidationIssue(
                            rule_id="SER-001",
                            severity=ValidationSeverity.FATAL,
                            category=ValidationCategory.SERIALIZATION,
                            message=f"Invalid JSON at line {line_num}: {e}",
                            dataset_name=dataset_name,
                            record_index=line_num,
                        )
                    )
                    if len(all_issues) >= max_issues:
                        break
                    continue

                if not isinstance(record, dict):
                    all_issues.append(
                        ValidationIssue(
                            rule_id="SER-001",
                            severity=ValidationSeverity.FATAL,
                            category=ValidationCategory.SERIALIZATION,
                            message=f"Record at line {line_num} is not a JSON object",
                            dataset_name=dataset_name,
                            record_index=line_num,
                        )
                    )
                    if len(all_issues) >= max_issues:
                        break
                    continue

                # Run rules with schema
                result = RecordValidator.validate(
                    record=record,
                    dataset_name=dataset_name,
                    record_index=line_num,
                    rules=rules,
                    context=context,
                    schema=schema,
                )
                all_issues.extend(result.issues)
                records_validated += 1

                if len(all_issues) >= max_issues:
                    logger.warning(
                        "Issue cap (%d) reached for %s. Stopping validation.",
                        max_issues,
                        dataset_name,
                    )
                    break

        # Dataset-level finalize hooks (e.g. Approval production-scale gate)
        if len(all_issues) < max_issues:
            for rule in rules:
                finalize = getattr(rule, "finalize", None)
                if not callable(finalize):
                    continue
                try:
                    finalized = finalize(
                        dataset_name=dataset_name,
                        records_validated=records_validated,
                    )
                except TypeError:
                    continue
                if finalized:
                    all_issues.extend(finalized)

        duration_ms = (time.perf_counter() - start) * 1000
        has_fatal_or_error = any(
            i.severity in (ValidationSeverity.FATAL, ValidationSeverity.ERROR) for i in all_issues
        )
        status = ValidationStatus.FAILED if has_fatal_or_error else ValidationStatus.PASSED

        schema_info = f" (schema: {schema.schema_id})" if schema else ""
        logger.info(
            "Validated %s%s: %d records, %d issues (%s) in %.1fms",
            dataset_name,
            schema_info,
            records_validated,
            len(all_issues),
            status.value,
            duration_ms,
        )

        return ValidationResult(
            status=status,
            issues=tuple(all_issues),
            dataset_name=dataset_name,
            records_validated=records_validated,
            duration_ms=duration_ms,
        )
