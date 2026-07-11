"""Query plugin to locate Model definitions."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType


class FindModelQuery(BaseContextQuery):
    """
    Generates queries asking where a specific Odoo Model is defined.

    Supported Node Types: NodeType.MODEL
    Generated Question: "Where is model X defined?"
    """

    query_type = QueryType.FIND_MODEL
    supported_node_types = [NodeType.MODEL]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        for node in graph.find_nodes_by_type(NodeType.MODEL):
            queries.append(
                Query(
                    query_type=self.query_type,
                    intent=QueryIntent.FIND_MODEL,
                    target_node=node.node_id,
                    target_symbol=node.name,
                    natural_language=f"Where is model {node.name} defined?",
                    metadata=MappingProxyType(
                        {"module": node.module, "language": node.language.value}
                    ),
                )
            )
        return queries
