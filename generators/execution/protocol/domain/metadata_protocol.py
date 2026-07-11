"""Metadata protocol serialization model."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class MetadataProtocol:
    """
    Immutable representation of metadata for the protocol.

    Attributes:
        protocol_version: The version of the protocol schema used.
        schema_version: The version of the underlying schema.
        compatibility_version: The lowest version this payload is compatible with.
        timestamp: Optional timestamp of creation.
    """

    protocol_version: str
    schema_version: str
    compatibility_version: str
    timestamp: str = field(default="")
