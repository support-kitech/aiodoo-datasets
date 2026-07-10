"""Base interface for Relationship Extractors."""

from aiodoo_datasets.generators.context.analysis.knowledge import ContextKnowledge
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, LanguageType
from aiodoo_datasets.generators.context.analysis.graph.edge import ContextEdge
from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph

class BaseRelationshipExtractor:
    """
    Base interface for all relationship extractors.
    
    Responsibilities:
    - Defines the supported languages and the exact RelationshipType.
    - Deterministically extracts ContextEdges from a pre-populated ContextGraph
      using structural knowledge (e.g. AST, XML).
      
    This class never mutates the graph directly, it only yields edges for the orchestrator.
    """
    relation_type: RelationshipType
    supported_languages: list[LanguageType]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        """
        Extract edges based on the knowledge provided.
        
        Args:
            graph: The current ContextGraph containing nodes.
            knowledge: Strongly typed container containing parsed artifacts.
            
        Returns:
            A list of new ContextEdge objects.
        """
        raise NotImplementedError("Extractors must implement extract()")
