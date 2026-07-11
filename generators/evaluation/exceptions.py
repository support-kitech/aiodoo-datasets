"""Custom exceptions for Evaluation Generator."""

class EvaluationGeneratorError(Exception):
    """Base exception for all Evaluation Generator errors."""
    pass

class EvaluationValidationError(EvaluationGeneratorError):
    """Raised when evaluation object validation fails."""
    pass

class EvaluationPipelineError(EvaluationGeneratorError):
    """Raised when the evaluation pipeline encounters a critical error."""
    pass
