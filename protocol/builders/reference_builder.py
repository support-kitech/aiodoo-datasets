"""ReferenceBuilder for the Protocol Framework."""

from protocol.builders.base import BaseBuilder, IdentifierFactory
from protocol.domain.enums import ReferenceType
from protocol.domain.references import ProtocolReference


class ReferenceBuilder(BaseBuilder):
    """Stateless builder that constructs immutable ProtocolReference objects."""

    @staticmethod
    def build(
        reference_type: ReferenceType,
        target_identifier: str,
        *,
        identifier_components: tuple[str, ...] = (),
    ) -> ProtocolReference:
        """
        Build an immutable ProtocolReference.

        Args:
            reference_type: The type of entity being referenced.
            target_identifier: The canonical hash or path of the target.
            identifier_components: Additional components for deterministic ID.

        Returns:
            A frozen ProtocolReference instance.
        """
        components = identifier_components or (reference_type.value, target_identifier)
        pid = IdentifierFactory.for_reference(*components)
        return ProtocolReference(
            identifier=pid,
            reference_type=reference_type,
            target_identifier=target_identifier,
        )
