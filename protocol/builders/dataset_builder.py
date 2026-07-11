"""DatasetBuilder for the Protocol Framework."""

from protocol.builders.base import BaseBuilder, IdentifierFactory
from protocol.domain.base import ProtocolObject
from protocol.domain.dataset import ProtocolDataset
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.schema import ProtocolSchema


class DatasetBuilder(BaseBuilder):
    """Stateless builder that constructs immutable ProtocolDataset objects."""

    @staticmethod
    def build(
        manifest: ProtocolManifest,
        schema: ProtocolSchema,
        *,
        items: tuple[ProtocolObject, ...] = (),
        identifier_components: tuple[str, ...] = (),
    ) -> ProtocolDataset:
        """
        Build an immutable ProtocolDataset.

        Args:
            manifest: The dataset manifest.
            schema: The dataset schema.
            items: Tuple of protocol objects belonging to this dataset.
            identifier_components: Additional components for deterministic ID.

        Returns:
            A frozen ProtocolDataset instance.
        """
        components = identifier_components or (
            manifest.identifier.hash_value,
            schema.identifier.hash_value,
        )
        pid = IdentifierFactory.for_dataset(*components)
        return ProtocolDataset(
            identifier=pid,
            manifest=manifest,
            schema=schema,
            items=items,
        )
