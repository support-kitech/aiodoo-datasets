"""Reference models for the Protocol Framework."""

from dataclasses import dataclass

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType, ReferenceType


@dataclass(frozen=True, slots=True)
class ProtocolReference(ProtocolObject):
    """
    A unified pointer to an entity (repository, file, dataset).
    Replaces fragmented references across generators.
    """

    reference_type: ReferenceType
    target_identifier: str

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.REFERENCE
