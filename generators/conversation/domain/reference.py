"""Reference domain model for Conversation Generator."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Reference:
    """A strict traceable link to an upstream protocol node."""

    source_generator: str
    source_reference: str
    description: str
