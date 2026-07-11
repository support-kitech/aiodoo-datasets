"""Metadata models for the Protocol Framework."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType


@dataclass(frozen=True, slots=True)
class ProtocolMetadata(ProtocolObject):
    """
    Unified metadata model capturing properties of a dataset or artifact.
    Replaces disjointed metadata dicts across generators.
    """

    properties: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.METADATA
