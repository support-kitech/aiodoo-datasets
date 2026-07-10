"""Extracts computation dependencies."""

from aiodoo_datasets.generators.context.analysis.knowledge import ContextKnowledge
from aiodoo_datasets.generators.context.analysis.relationships.base import BaseRelationshipExtractor
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, LanguageType
from aiodoo_datasets.generators.context.analysis.graph.edge import ContextEdge
from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph

class ComputesRelationship(BaseRelationshipExtractor):
    """
    Extracts computation links (e.g. Field compute="_compute_foo" -> Method).
    
    Supported Knowledge: Python AST.
    """
    relation_type = RelationshipType.COMPUTES
    supported_languages = [LanguageType.PYTHON]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        edges = []
        return edges
