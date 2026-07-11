"""Extracts user interaction triggers."""

from generators.context.analysis.knowledge import ContextKnowledge
from generators.context.analysis.relationships.base import BaseRelationshipExtractor
from generators.context.analysis.graph.enums import RelationshipType, LanguageType
from generators.context.analysis.graph.edge import ContextEdge
from generators.context.analysis.graph.graph import ContextGraph


class TriggersRelationship(BaseRelationshipExtractor):  # type: ignore[misc]
    """
    Extracts action triggers (e.g. Menu -> Action, Action -> View).

    Supported Knowledge: XML trees.
    """

    relation_type = RelationshipType.TRIGGERS
    supported_languages = [LanguageType.XML]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        edges = []  # type: ignore[var-annotated]
        return edges
