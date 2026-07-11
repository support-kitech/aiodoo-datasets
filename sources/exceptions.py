"""Exceptions for the Sources Framework."""


class SourcesError(Exception):
    """Base exception for all Sources Framework errors."""
    pass


class ConfigurationError(SourcesError):
    """Raised when sources.yaml or versions.yaml is invalid or missing."""
    pass


class ValidationError(SourcesError):
    """Raised when configuration, repository, or manifest validation fails."""
    pass


class RepositoryError(SourcesError):
    """Raised when a requested repository or path cannot be found or handled."""
    pass


class ScannerError(SourcesError):
    """Raised when filesystem traversal or discovery fails."""
    pass


class CacheError(SourcesError):
    """Raised when the cache cannot be read or written."""
    pass
