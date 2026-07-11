"""ManifestBuilder for the Protocol Framework."""

from protocol.builders.base import BaseBuilder, IdentifierFactory
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.metadata import ProtocolMetadata
from protocol.domain.references import ProtocolReference
from protocol.domain.version import ProtocolVersion


class ManifestBuilder(BaseBuilder):
    """Stateless builder that constructs immutable ProtocolManifest objects."""

    @staticmethod
    def build(
        version: ProtocolVersion,
        metadata: ProtocolMetadata,
        repository_reference: ProtocolReference,
        *,
        statistics_reference: ProtocolReference | None = None,
        dependencies: tuple[ProtocolReference, ...] = (),
        identifier_components: tuple[str, ...] = (),
    ) -> ProtocolManifest:
        """
        Build an immutable ProtocolManifest.

        Args:
            version: The protocol version triplet.
            metadata: The dataset metadata.
            repository_reference: The reference to the source repository.
            statistics_reference: Optional statistics reference.
            dependencies: Tuple of dependency references.
            identifier_components: Additional components for deterministic ID.

        Returns:
            A frozen ProtocolManifest instance.
        """
        components = identifier_components or (
            version.identifier.hash_value,
            repository_reference.identifier.hash_value,
        )
        pid = IdentifierFactory.for_manifest(*components)
        return ProtocolManifest(
            identifier=pid,
            version=version,
            metadata=metadata,
            repository_reference=repository_reference,
            statistics_reference=statistics_reference,
            dependencies=dependencies,
        )
