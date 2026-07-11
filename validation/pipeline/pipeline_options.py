"""Execution options for the Validation Framework."""

from dataclasses import dataclass

from validation.domain.enums import ValidationCategory, ValidationSeverity, ReportFormat


@dataclass(frozen=True, slots=True)
class ValidationOptions:
    """Immutable options for configuring a validation pass."""

    fail_fast: bool = False
    parallel: bool = True
    workers: int = 4
    categories: tuple[ValidationCategory, ...] = ()
    severity_threshold: ValidationSeverity = ValidationSeverity.WARNING
    report_format: ReportFormat = ReportFormat.CONSOLE
    max_issues_per_dataset: int = 1000
    # Stage toggles
    validate_schemas: bool = True
    validate_datasets: bool = True
    validate_manifests: bool = True
    validate_cross_dataset: bool = True
