"""Immutable result models for the Validation Framework."""

from dataclasses import dataclass, field
from typing import Mapping
from types import MappingProxyType

from validation.domain.enums import ValidationStatus, ValidationSeverity
from validation.domain.models import ValidationIssue


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Immutable result of validating a single dataset."""

    status: ValidationStatus
    issues: tuple[ValidationIssue, ...] = ()
    dataset_name: str = ""
    records_validated: int = 0
    duration_ms: float = 0.0

    @staticmethod
    def success(
        *, dataset_name: str = "", records_validated: int = 0, duration_ms: float = 0.0
    ) -> "ValidationResult":
        """Create a passing result."""
        return ValidationResult(
            status=ValidationStatus.PASSED,
            dataset_name=dataset_name,
            records_validated=records_validated,
            duration_ms=duration_ms,
        )

    @staticmethod
    def failure(
        *issues: ValidationIssue,
        dataset_name: str = "",
        records_validated: int = 0,
        duration_ms: float = 0.0,
    ) -> "ValidationResult":
        """Create a failing result with issues."""
        return ValidationResult(
            status=ValidationStatus.FAILED,
            issues=issues,
            dataset_name=dataset_name,
            records_validated=records_validated,
            duration_ms=duration_ms,
        )

    @staticmethod
    def skipped(*, dataset_name: str = "", reason: str = "") -> "ValidationResult":
        """Create a skipped result."""
        return ValidationResult(
            status=ValidationStatus.SKIPPED,
            dataset_name=dataset_name,
        )

    def merge(self, other: "ValidationResult") -> "ValidationResult":
        """Combine two results. Failed if either failed."""
        merged_status = (
            ValidationStatus.FAILED
            if self.status == ValidationStatus.FAILED or other.status == ValidationStatus.FAILED
            else ValidationStatus.PASSED
        )
        return ValidationResult(
            status=merged_status,
            issues=self.issues + other.issues,
            dataset_name=self.dataset_name or other.dataset_name,
            records_validated=self.records_validated + other.records_validated,
            duration_ms=self.duration_ms + other.duration_ms,
        )

    @property
    def fatal_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.FATAL)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.WARNING)


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    """Aggregate summary across all validated datasets."""

    total_datasets: int = 0
    total_records: int = 0
    total_issues: int = 0
    fatal_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    passed: bool = True
    duration_ms: float = 0.0
    # Per-category and per-generator breakdowns (Issue 5)
    per_category_counts: Mapping[str, int] = field(
        default_factory=lambda: MappingProxyType({})
    )
    per_generator_counts: Mapping[str, int] = field(
        default_factory=lambda: MappingProxyType({})
    )
    health_score: float = 100.0


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Complete validation report containing all results and summary."""

    results: tuple[ValidationResult, ...] = ()
    summary: ValidationSummary = field(default_factory=ValidationSummary)
    framework_version: str = ""
    timestamp: str = ""
    options: Mapping[str, object] = field(default_factory=lambda: MappingProxyType({}))
