"""Query plugin to locate the action that opens a target."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType, RelationshipType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType

class FindActionQuery(BaseContextQuery):
    """
    Generates queries asking which action opens a target (like a view or model).
    
    Supported Node Types: NodeType.ACTION
    Generated Question: "Which action opens X?"
    """
    query_type = QueryType.FIND_ACTION
    supported_node_types = [NodeType.ACTION]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        # Target nodes that have an incoming OPENS relationship from an ACTION node.
        # But wait, we might not have 'opens' edge, maybe TRIGGERS? The prompt says "Which action opens X?"
        # The relationship framework uses TRIGGERS for Menu->Action, Action->View. Let's use TRIGGERS.
        for edge in graph.find_edges_by_type(RelationshipType.TRIGGERS):
            source_node = graph.get_node(edge.source_id)
            if source_node.node_type == NodeType.ACTION:
                target_node = graph.get_node(edge.target_id)
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_ACTION,
                        target_node=target_node.node_id,
                        target_symbol=target_node.name,
                        natural_language=f"Which action opens {target_node.name}?",
                        metadata=MappingProxyType({"module": source_node.module, "language": source_node.language.value})
                    )
                )
        return queries
