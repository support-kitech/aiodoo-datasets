"""Exceptions for the Export package."""


class ExportError(Exception):
    """Base exception for export errors."""

    pass


class WriterError(ExportError):
    """Raised when writing to disk fails."""

    pass


class ExportValidationError(ExportError):
    """Raised when export validation fails."""

    pass
