"""
AIODOO Validation Framework

The shared validation system for all AIODOO dataset generators.
Validates every dataset after generation and before statistics/export.

Supports generator-aware schema resolution, deterministic rule execution,
and multi-format reporting.
"""

from validation.constants.framework import VALIDATION_FRAMEWORK_VERSION
from validation.exceptions import (
    ValidationError,
    ValidationConfigurationError,
    ValidationRuleError,
    ValidationPipelineError,
)
from validation.domain.enums import (
    ValidationSeverity,
    ValidationStatus,
    ValidationCategory,
    RuleScope,
    ReportFormat,
)
from validation.domain.models import ValidationIssue, ValidationContext
from validation.domain.results import ValidationResult, ValidationSummary, ValidationReport
from validation.domain.metrics import ValidationMetrics
from validation.schemas.base import DatasetSchema, FieldDefinition
from validation.schemas.registry import SchemaRegistry
from validation.pipeline.pipeline_options import ValidationOptions
from validation.pipeline.pipeline_result import PipelineResult
from validation.core.manager import ValidationManager

__version__ = VALIDATION_FRAMEWORK_VERSION

__all__ = [
    # Framework
    "VALIDATION_FRAMEWORK_VERSION",
    "__version__",
    # Exceptions
    "ValidationError",
    "ValidationConfigurationError",
    "ValidationRuleError",
    "ValidationPipelineError",
    # Enums
    "ValidationSeverity",
    "ValidationStatus",
    "ValidationCategory",
    "RuleScope",
    "ReportFormat",
    # Domain Models
    "ValidationIssue",
    "ValidationContext",
    "ValidationResult",
    "ValidationSummary",
    "ValidationReport",
    "ValidationMetrics",
    # Schema Framework
    "DatasetSchema",
    "FieldDefinition",
    "SchemaRegistry",
    # Pipeline
    "ValidationOptions",
    "PipelineResult",
    # Manager
    "ValidationManager",
]
