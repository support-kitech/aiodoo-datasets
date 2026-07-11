"""Validates a single deserialized record against applicable rules."""

from validation.domain.enums import ValidationStatus
from validation.domain.models import ValidationIssue, ValidationContext
from validation.domain.results import ValidationResult
from validation.rules.base import BaseRule
from validation.schemas.base import DatasetSchema


class RecordValidator:
    """Validates a single deserialized record dict against a set of rules."""

    @staticmethod
    def validate(
        record: dict,  # type: ignore[type-arg]
        dataset_name: str,
        record_index: int,
        rules: tuple[BaseRule, ...],
        context: ValidationContext,
        schema: DatasetSchema | None = None,
    ) -> ValidationResult:
        """
        Execute all applicable rules against a single record.

        Args:
            record: The deserialized JSONL record.
            dataset_name: Name of the dataset file.
            record_index: 0-indexed line number in the JSONL file.
            rules: Sorted tuple of rules to execute.
            context: Immutable validation context.
            schema: Resolved schema for this dataset's generator.

        Returns:
            ValidationResult with all collected issues.
        """
        from types import MappingProxyType

        # Build a record-scoped context with schema, dataset name, and index
        meta_dict = dict(context.metadata)
        meta_dict["current_dataset"] = dataset_name
        meta_dict["current_index"] = record_index
        if schema is not None:
            meta_dict["resolved_schema"] = schema

        record_context = ValidationContext(
            dataset_dir=context.dataset_dir,
            dataset_files=context.dataset_files,
            manifest_files=context.manifest_files,
            statistics_files=context.statistics_files,
            protocol_context=context.protocol_context,
            metadata=MappingProxyType(meta_dict),
        )

        all_issues: list[ValidationIssue] = []
        for rule in rules:
            issues = rule.validate(record, record_context)
            all_issues.extend(issues)

        status = (
            ValidationStatus.FAILED
            if any(i.severity.value in ("fatal", "error") for i in all_issues)
            else ValidationStatus.PASSED
        )

        return ValidationResult(
            status=status,
            issues=tuple(all_issues),
            dataset_name=dataset_name,
            records_validated=1,
        )
