"""Query plugin to locate the menu that opens a target."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType, RelationshipType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType

class FindMenuQuery(BaseContextQuery):
    """
    Generates queries asking which menu opens an action.
    
    Supported Node Types: NodeType.MENU
    Generated Question: "Which menu opens X?"
    """
    query_type = QueryType.FIND_MENU
    supported_node_types = [NodeType.MENU]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        # Target nodes that have an incoming TRIGGERS relationship from a MENU node.
        for edge in graph.find_edges_by_type(RelationshipType.TRIGGERS):
            source_node = graph.get_node(edge.source_id)
            if source_node.node_type == NodeType.MENU:
                target_node = graph.get_node(edge.target_id)
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_MENU,
                        target_node=target_node.node_id,
                        target_symbol=target_node.name,
                        natural_language=f"Which menu opens {target_node.name}?",
                        metadata=MappingProxyType({"module": source_node.module, "language": source_node.language.value})
                    )
                )
        return queries
