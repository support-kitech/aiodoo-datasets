"""Query plugin to locate Field definitions."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType


class FindFieldQuery(BaseContextQuery):  # type: ignore[misc]
    """
    Generates queries asking where a specific Odoo Field is defined.

    Supported Node Types: NodeType.FIELD
    Generated Question: "Where is field X defined?"
    """

    query_type = QueryType.FIND_FIELD
    supported_node_types = [NodeType.FIELD]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        for node in graph.find_nodes_by_type(NodeType.FIELD):
            queries.append(
                Query(
                    query_type=self.query_type,
                    intent=QueryIntent.FIND_FIELD,
                    target_node=node.node_id,
                    target_symbol=node.name,
                    natural_language=f"Where is field {node.name} defined?",
                    metadata=MappingProxyType(
                        {"module": node.module, "language": node.language.value}
                    ),
                )
            )
        return queries
