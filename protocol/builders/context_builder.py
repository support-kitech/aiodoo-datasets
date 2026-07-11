"""ContextBuilder for the Protocol Framework."""

from protocol.builders.base import BaseBuilder
from protocol.domain.dataset import ProtocolContext, ProtocolDataset
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship


class ContextBuilder(BaseBuilder):
    """Stateless builder that constructs the root ProtocolContext graph."""

    @staticmethod
    def build(
        dataset: ProtocolDataset,
        *,
        relationships: tuple[ProtocolRelationship, ...] = (),
        references: tuple[ProtocolReference, ...] = (),
    ) -> ProtocolContext:
        """
        Build an immutable ProtocolContext.

        Args:
            dataset: The root dataset object.
            relationships: All directed edges in this protocol graph.
            references: All standalone references in this protocol graph.

        Returns:
            A frozen ProtocolContext instance.
        """
        return ProtocolContext(
            dataset=dataset,
            relationships=relationships,
            references=references,
        )
