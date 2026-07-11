"""Extracts inheritance relationships."""

from generators.context.analysis.knowledge import ContextKnowledge
from generators.context.analysis.relationships.base import BaseRelationshipExtractor
from generators.context.analysis.graph.enums import RelationshipType, LanguageType
from generators.context.analysis.graph.edge import ContextEdge
from generators.context.analysis.graph.graph import ContextGraph


class InheritsRelationship(BaseRelationshipExtractor):  # type: ignore[misc]
    """
    Extracts extension relationships (e.g. _inherit in Python, inherit_id in XML).

    Supported Knowledge: Python AST and XML trees.
    """

    relation_type = RelationshipType.INHERITS
    supported_languages = [LanguageType.PYTHON, LanguageType.XML]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        edges = []  # type: ignore[var-annotated]
        return edges
