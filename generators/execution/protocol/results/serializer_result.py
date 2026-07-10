"""Serializer result objects."""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SerializerResult:
    """
    Immutable result from ProtocolSerializer.
    
    Attributes:
        success: Whether serialization was successful.
        serialized_data: The serialized protocol string.
        diagnostics: Any diagnostic messages.
    """
    success: bool
    serialized_data: str = ""
    diagnostics: tuple[str, ...] = tuple()
