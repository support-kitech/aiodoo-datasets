"""Dataset and Context models for the Protocol Framework."""

from dataclasses import dataclass

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship
from protocol.domain.schema import ProtocolSchema


@dataclass(frozen=True, slots=True)
class ProtocolDataset(ProtocolObject):
    """
    The canonical representation of an AIODOO dataset.
    """

    manifest: ProtocolManifest
    schema: ProtocolSchema
    items: tuple[ProtocolObject, ...] = ()

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.DATASET


@dataclass(frozen=True, slots=True)
class ProtocolContext:
    """
    The root graph object passed to generators.
    Contains the dataset definition and the relational mapping.
    """

    dataset: ProtocolDataset
    relationships: tuple[ProtocolRelationship, ...] = ()
    references: tuple[ProtocolReference, ...] = ()
