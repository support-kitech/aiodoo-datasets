"""Query plugin to locate which security rules protect a target."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import NodeType, RelationshipType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery
from types import MappingProxyType

class FindSecurityQuery(BaseContextQuery):
    """
    Generates queries asking which ACL or Record Rule protects a model.
    
    Supported Node Types: NodeType.SECURITY_RULE, NodeType.ACL
    Generated Question: "Which ACL protects X?" or "Which Record Rule restricts X?"
    """
    query_type = QueryType.FIND_SECURITY
    supported_node_types = [NodeType.SECURITY_RULE, NodeType.ACL]

    def generate(self, graph: ContextGraph) -> list[Query]:
        queries = []
        # Target nodes that have an incoming SECURES relationship.
        for edge in graph.find_edges_by_type(RelationshipType.SECURES):
            source_node = graph.get_node(edge.source_id)
            target_node = graph.get_node(edge.target_id)
            
            if source_node.node_type == NodeType.ACL:
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_SECURITY,
                        target_node=target_node.node_id,
                        target_symbol=target_node.name,
                        natural_language=f"Which ACL protects {target_node.name}?",
                        metadata=MappingProxyType({
                            "module": source_node.module, 
                            "language": source_node.language.value,
                            "security_type": "acl"
                        })
                    )
                )
            elif source_node.node_type == NodeType.SECURITY_RULE:
                queries.append(
                    Query(
                        query_type=self.query_type,
                        intent=QueryIntent.FIND_SECURITY,
                        target_node=target_node.node_id,
                        target_symbol=target_node.name,
                        natural_language=f"Which Record Rule restricts {target_node.name}?",
                        metadata=MappingProxyType({
                            "module": source_node.module, 
                            "language": source_node.language.value,
                            "security_type": "record_rule"
                        })
                    )
                )
        return queries
