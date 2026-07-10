"""Base interface for Query Plugins."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType

class BaseContextQuery:
    """
    Base interface for all query plugins.
    
    Responsibilities:
    - Defines the supported node types and the exact QueryType.
    - Generates Query objects deterministically by inspecting the ContextGraph.
    - Does NOT traverse recursively. Only identifies valid targets.
    """
    query_type: QueryType
    supported_node_types: list[NodeType]

    def generate(self, graph: ContextGraph) -> list[Query]:
        """
        Generate queries based on the graph nodes/edges.
        
        Args:
            graph: The fully populated ContextGraph (nodes and edges).
            
        Returns:
            A list of new Query objects.
        """
        raise NotImplementedError("Query plugins must implement generate()")
