"""Query plugin to locate which view displays a symbol."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType, RelationshipType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType


class FindViewQuery(BaseContextQuery):
    """
    Generates queries asking which view displays a given element (like a field or model).

    Supported Node Types: NodeType.VIEW
    Generated Question: "Which view displays X?"
    """

    query_type = QueryType.FIND_VIEW
    supported_node_types = [NodeType.VIEW]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        # We look for all DISPLAY edges: View -> Target (Field/Model)
        for edge in graph.find_edges_by_type(RelationshipType.DISPLAYS):
            # Target is what is being displayed
            target_node = graph.get_node(edge.target_id)
            # Source is the view
            view_node = graph.get_node(edge.source_id)

            if view_node.node_type == NodeType.VIEW:
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_VIEW,
                        target_node=target_node.node_id,
                        target_symbol=target_node.name,
                        natural_language=f"Which view displays {target_node.name}?",
                        metadata=MappingProxyType(
                            {"module": view_node.module, "language": view_node.language.value}
                        ),
                    )
                )
        return queries
