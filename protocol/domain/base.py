"""Base models for the Protocol Framework."""

from dataclasses import dataclass

from protocol.domain.identifiers import ProtocolIdentifier


@dataclass(frozen=True, slots=True)
class ProtocolObject:
    """
    The root interface for all Protocol objects.
    Enforces the presence of a deterministic identifier.
    Subclasses provide their own domain-specific fields.
    """

    identifier: ProtocolIdentifier
