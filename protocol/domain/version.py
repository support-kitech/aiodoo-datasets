"""Version models for the Protocol Framework."""

from dataclasses import dataclass

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType


@dataclass(frozen=True, slots=True)
class ProtocolVersion(ProtocolObject):
    """
    Standardized version triplet encapsulating the state of the system
    during dataset generation.
    """

    framework_version: str
    schema_version: str
    generator_version: str

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.VERSION
