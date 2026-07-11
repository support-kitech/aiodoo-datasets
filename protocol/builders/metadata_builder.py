"""MetadataBuilder for the Protocol Framework."""

from types import MappingProxyType
from typing import Any, Mapping

from protocol.builders.base import BaseBuilder, IdentifierFactory
from protocol.domain.metadata import ProtocolMetadata


class MetadataBuilder(BaseBuilder):
    """Stateless builder that constructs immutable ProtocolMetadata objects."""

    @staticmethod
    def build(
        properties: Mapping[str, Any],
        *,
        identifier_components: tuple[str, ...] = (),
    ) -> ProtocolMetadata:
        """
        Build an immutable ProtocolMetadata from a property mapping.

        Args:
            properties: Key-value metadata pairs.
            identifier_components: Additional components for deterministic ID.

        Returns:
            A frozen ProtocolMetadata instance.
        """
        frozen_props = MappingProxyType(dict(properties))
        pid = IdentifierFactory.for_metadata(*identifier_components)
        return ProtocolMetadata(identifier=pid, properties=frozen_props)
