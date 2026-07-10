"""Exceptions for the Protocol package."""

class ProtocolError(Exception):
    """Base exception for protocol errors."""
    pass

class MappingError(ProtocolError):
    """Raised when mapping fails."""
    pass

class SerializationError(ProtocolError):
    """Raised when serialization fails."""
    pass

class ValidationError(ProtocolError):
    """Raised when validation fails."""
    pass
