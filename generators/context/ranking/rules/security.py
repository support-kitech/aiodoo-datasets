"""Security Ranking Rule."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, NodeType
from aiodoo_datasets.generators.context.generation.query import Query, QueryType
from aiodoo_datasets.generators.context.ranking.enums import RankingRuleType, RankingScore, RankingReason
from aiodoo_datasets.generators.context.ranking.result import RankingResult
from aiodoo_datasets.generators.context.ranking.base import BaseRankingRule
from aiodoo_datasets.generators.context.ranking.utils import freeze_metadata

class SecurityRule(BaseRankingRule):
    """
    Ranks security rules (ACL, Record Rules, Groups).
    
    Engineering Purpose:
        Identifies security mechanisms protecting a target model.
        Scores (70).
        
    Supported Queries:
        FIND_SECURITY
        
    Limitations:
        Specifically looks for SECURES edges pointing to the query target.
    """
    rule_type = RankingRuleType.SECURITY
    supported_query_types = [QueryType.FIND_SECURITY]

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        results = []
        if query.query_type in self.supported_query_types:
            for edge in graph.find_edges_by_type(RelationshipType.SECURES):
                if edge.target_id == query.target_node:
                    source_node = graph.get_node(edge.source_id)
                    if source_node.node_type in [NodeType.ACL, NodeType.SECURITY_RULE]:
                        results.append(
                            RankingResult(
                                query_id=query.query_id,
                                node_id=source_node.node_id,
                                score=RankingScore.SECURITY,
                                matched_rule=self.rule_type,
                                reason=RankingReason.SECURITY_REFERENCE,
                                metadata=freeze_metadata({
                                    "module": source_node.module,
                                    "language": source_node.language.value,
                                    "relative_path": source_node.relative_path,
                                    "start_line": 0,
                                    "matched_relationship": edge.relationship_type.value,
                                    "secures": query.target_symbol
                                })
                            )
                        )
        return results
