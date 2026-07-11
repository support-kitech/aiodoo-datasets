"""Exception hierarchy for the Protocol Framework."""


class ProtocolError(Exception):
    """Base exception for all Protocol Framework errors."""

    pass


class ProtocolValidationError(ProtocolError):
    """Raised when a protocol object violates structural integrity."""

    pass
