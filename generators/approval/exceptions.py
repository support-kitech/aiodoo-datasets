"""Exceptions for the Approval Generator."""


class ApprovalGeneratorError(Exception):
    """Base exception for all Approval Generator errors."""

    pass


class AnalysisError(ApprovalGeneratorError):
    """Raised when protocol ingestion or analysis fails."""

    pass


class RuleEvaluationError(ApprovalGeneratorError):
    """Raised when a rule plugin fails to execute properly."""

    pass


class ValidationException(ApprovalGeneratorError):
    """Raised when validation constraints are violated."""

    pass


class ProtocolMappingError(ApprovalGeneratorError):
    """Raised when domain objects cannot be mapped to protocol serialization formats."""

    pass


class ApprovalValidationError(ValidationException):
    """Raised when validation constraints are violated in the dataset."""

    pass


class ApprovalPipelineError(ApprovalGeneratorError):
    """Raised when the pipeline fails to execute."""

    pass
