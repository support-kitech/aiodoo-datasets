"""RelationshipBuilder for the Protocol Framework."""

from protocol.builders.base import BaseBuilder, IdentifierFactory
from protocol.domain.enums import RelationshipType
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship


class RelationshipBuilder(BaseBuilder):
    """Stateless builder that constructs immutable ProtocolRelationship objects."""

    @staticmethod
    def build(
        relationship_type: RelationshipType,
        source: ProtocolReference,
        target: ProtocolReference,
        *,
        identifier_components: tuple[str, ...] = (),
    ) -> ProtocolRelationship:
        """
        Build an immutable ProtocolRelationship.

        Args:
            relationship_type: The kind of relationship (PARENT, CHILD, etc.).
            source: The source reference of the directed edge.
            target: The target reference of the directed edge.
            identifier_components: Additional components for deterministic ID.

        Returns:
            A frozen ProtocolRelationship instance.
        """
        components = identifier_components or (
            relationship_type.value,
            source.identifier.hash_value,
            target.identifier.hash_value,
        )
        pid = IdentifierFactory.for_relationship(*components)
        return ProtocolRelationship(
            identifier=pid,
            relationship_type=relationship_type,
            source=source,
            target=target,
        )
