"""Exceptions for the Conversation Generator."""


class ConversationError(Exception):
    """Base exception for all Conversation Generator errors."""

    pass


class ConversationValidationError(ConversationError):
    """Raised when domain or protocol validation fails."""

    pass


class ConversationPipelineError(ConversationError):
    """Raised when the conversation pipeline fails."""

    pass


class ParserError(ConversationError):
    """Raised when a protocol parser fails to extract evidence."""

    pass
