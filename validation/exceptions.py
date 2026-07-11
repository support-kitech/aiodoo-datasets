"""Exception hierarchy for the Validation Framework."""


class ValidationError(Exception):
    """Base exception for all Validation Framework errors."""

    pass


class ValidationConfigurationError(ValidationError):
    """Raised when validation options or configuration are invalid."""

    pass


class ValidationRuleError(ValidationError):
    """Raised when a rule implementation encounters an internal error."""

    pass


class ValidationPipelineError(ValidationError):
    """Raised when the validation pipeline orchestration fails."""

    pass
