"""Extracts UI display relationships."""

from aiodoo_datasets.generators.context.analysis.knowledge import ContextKnowledge
from aiodoo_datasets.generators.context.analysis.relationships.base import BaseRelationshipExtractor
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, LanguageType
from aiodoo_datasets.generators.context.analysis.graph.edge import ContextEdge
from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph


class DisplaysRelationship(BaseRelationshipExtractor):  # type: ignore[misc]
    """
    Extracts display relationships (e.g. View -> Field, View -> Model).

    Supported Knowledge: XML trees.
    """

    relation_type = RelationshipType.DISPLAYS
    supported_languages = [LanguageType.XML]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        edges = []  # type: ignore[var-annotated]
        return edges
