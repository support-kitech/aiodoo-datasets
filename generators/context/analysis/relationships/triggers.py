"""Extracts user interaction triggers."""

from aiodoo_datasets.generators.context.analysis.knowledge import ContextKnowledge
from aiodoo_datasets.generators.context.analysis.relationships.base import BaseRelationshipExtractor
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, LanguageType
from aiodoo_datasets.generators.context.analysis.graph.edge import ContextEdge
from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph

class TriggersRelationship(BaseRelationshipExtractor):
    """
    Extracts action triggers (e.g. Menu -> Action, Action -> View).
    
    Supported Knowledge: XML trees.
    """
    relation_type = RelationshipType.TRIGGERS
    supported_languages = [LanguageType.XML]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        edges = []
        return edges
