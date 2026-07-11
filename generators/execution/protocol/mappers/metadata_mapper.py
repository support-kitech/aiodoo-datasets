"""Mapper for metadata."""

from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext
from aiodoo_datasets.generators.execution.protocol.domain.metadata_protocol import MetadataProtocol
from aiodoo_datasets.generators.execution.protocol import version


class MetadataMapper:
    """Maps context to MetadataProtocol."""

    @staticmethod
    def map(context: ProtocolContext) -> MetadataProtocol:
        """Create a metadata protocol object."""
        return MetadataProtocol(
            protocol_version=context.protocol_version,
            schema_version=version.schema_version,
            compatibility_version=version.compatibility_version,
        )
