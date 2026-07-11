"""Schema models for the Protocol Framework."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from protocol.domain.base import ProtocolObject
from protocol.domain.enums import ProtocolType


@dataclass(frozen=True, slots=True)
class ProtocolSchema(ProtocolObject):
    """
    Versioned schema definition that datasets must conform to.
    Consumed by the Validation Framework.
    """

    schema_version: str
    schema_definition: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.SCHEMA
