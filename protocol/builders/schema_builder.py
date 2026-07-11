"""SchemaBuilder for the Protocol Framework."""

from types import MappingProxyType
from typing import Any, Mapping

from protocol.builders.base import BaseBuilder, IdentifierFactory
from protocol.domain.schema import ProtocolSchema


class SchemaBuilder(BaseBuilder):
    """Stateless builder that constructs immutable ProtocolSchema objects."""

    @staticmethod
    def build(
        schema_version: str,
        schema_definition: Mapping[str, Any] | None = None,
        *,
        identifier_components: tuple[str, ...] = (),
    ) -> ProtocolSchema:
        """
        Build an immutable ProtocolSchema.

        Args:
            schema_version: The version string for this schema.
            schema_definition: The schema definition mapping.
            identifier_components: Additional components for deterministic ID.

        Returns:
            A frozen ProtocolSchema instance.
        """
        definition = MappingProxyType(dict(schema_definition or {}))
        components = identifier_components or (schema_version,)
        pid = IdentifierFactory.for_schema(*components)
        return ProtocolSchema(
            identifier=pid,
            schema_version=schema_version,
            schema_definition=definition,
        )
