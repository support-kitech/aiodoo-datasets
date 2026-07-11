"""Enumerations for the Validation Framework."""

from enum import Enum


class ValidationSeverity(str, Enum):
    """Severity level of a validation issue."""

    FATAL = "fatal"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationStatus(str, Enum):
    """Outcome status of a validation pass."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class ValidationCategory(str, Enum):
    """Category grouping for validation rules."""

    SCHEMA = "schema"
    METADATA = "metadata"
    INTEGRITY = "integrity"
    REFERENCES = "references"
    SERIALIZATION = "serialization"
    GENERATOR = "generator"
    CROSS_DATASET = "cross_dataset"


class RuleScope(str, Enum):
    """Scope of a validation rule."""

    UNIVERSAL = "universal"
    GENERATOR_SPECIFIC = "generator_specific"


class ReportFormat(str, Enum):
    """Output format for validation reports."""

    CONSOLE = "console"
    JSON = "json"
    MARKDOWN = "markdown"
    CI = "ci"
