"""Manifest models for the Protocol Framework."""

from dataclasses import dataclass

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType
from protocol.domain.metadata import ProtocolMetadata
from protocol.domain.references import ProtocolReference
from protocol.domain.version import ProtocolVersion


@dataclass(frozen=True, slots=True)
class ProtocolManifest(ProtocolObject):
    """
    High-level summary describing the generated dataset.
    """

    version: ProtocolVersion
    metadata: ProtocolMetadata
    repository_reference: ProtocolReference
    statistics_reference: ProtocolReference | None = None
    dependencies: tuple[ProtocolReference, ...] = ()

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.MANIFEST
