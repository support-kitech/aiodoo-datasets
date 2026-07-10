"""Query plugin to locate module dependencies."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType, RelationshipType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType

class FindDependencyQuery(BaseContextQuery):
    """
    Generates queries asking which modules depend on a specific module.
    
    Supported Node Types: NodeType.MANIFEST
    Generated Question: "Which modules depend on X?"
    """
    query_type = QueryType.FIND_DEPENDENCY
    supported_node_types = [NodeType.MANIFEST]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        # Look for DEPENDS relationships (e.g. Manifest -> Manifest)
        # We generate "Which modules depend on X?" where X is the target of DEPENDS.
        for edge in graph.find_edges_by_type(RelationshipType.DEPENDS):
            target_node = graph.get_node(edge.target_id)
            source_node = graph.get_node(edge.source_id)
            
            if source_node.node_type == NodeType.MANIFEST and target_node.node_type == NodeType.MANIFEST:
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_DEPENDENCY,
                        target_node=target_node.node_id,
                        target_symbol=target_node.name, # Usually the module name
                        natural_language=f"Which modules depend on {target_node.name}?",
                        metadata=MappingProxyType({"module": source_node.module, "language": source_node.language.value})
                    )
                )
        return queries
