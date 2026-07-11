"""Relationship models for the Protocol Framework."""

from dataclasses import dataclass

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType, RelationshipType
from protocol.domain.references import ProtocolReference


@dataclass(frozen=True, slots=True)
class ProtocolRelationship(ProtocolObject):
    """
    A directed edge between two protocol references.
    """

    relationship_type: RelationshipType
    source: ProtocolReference
    target: ProtocolReference

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.RELATIONSHIP
