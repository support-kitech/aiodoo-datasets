"""Query plugin to locate compute method logic."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType, RelationshipType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType


class FindComputeQuery(BaseContextQuery):  # type: ignore[misc]
    """
    Generates queries asking where a field's computation logic resides.

    Supported Node Types: NodeType.FIELD
    Generated Question: "Where is field X computed?"
    """

    query_type = QueryType.FIND_COMPUTE
    supported_node_types = [NodeType.FIELD]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        # Target fields that have a COMPUTES outgoing edge.
        for node in graph.find_nodes_by_type(NodeType.FIELD):
            outgoing_edges = graph.get_outgoing_edges(node.node_id)
            has_compute = any(
                e.relationship_type == RelationshipType.COMPUTES for e in outgoing_edges
            )

            if has_compute:
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_COMPUTE,
                        target_node=node.node_id,
                        target_symbol=node.name,
                        natural_language=f"Where is field {node.name} computed?",
                        metadata=MappingProxyType(
                            {"module": node.module, "language": node.language.value}
                        ),
                    )
                )
        return queries
