"""Base exceptions for the Preprocessing Framework."""

class PreprocessingError(Exception):
    """Base exception for all preprocessing framework errors."""
    pass


class PreprocessingConfigError(PreprocessingError):
    """Raised when there is a configuration issue."""
    pass


class PreprocessingValidationError(PreprocessingError):
    """Raised when Stage 1 or Stage 2 validation fails."""
    pass


class PreprocessingCacheError(PreprocessingError):
    """Raised when there is an issue with the SQLite cache."""
    pass
