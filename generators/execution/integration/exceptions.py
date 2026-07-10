"""Exceptions for the Integration package."""

class IntegrationError(Exception):
    """Base exception for integration errors."""
    pass

class PipelineExecutionError(IntegrationError):
    """Raised when a pipeline stage fails."""
    pass

class PipelineValidationError(IntegrationError):
    """Raised when pipeline validation fails."""
    pass
