"""View Ranking Rule."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, NodeType
from aiodoo_datasets.generators.context.generation.query import Query, QueryType
from aiodoo_datasets.generators.context.ranking.enums import RankingRuleType, RankingScore, RankingReason
from aiodoo_datasets.generators.context.ranking.result import RankingResult
from aiodoo_datasets.generators.context.ranking.base import BaseRankingRule
from aiodoo_datasets.generators.context.ranking.utils import freeze_metadata

class ViewRule(BaseRankingRule):
    """
    Ranks XML Views.
    
    Engineering Purpose:
        Identifies views that display a field or model.
        Scores (70).
        
    Supported Queries:
        FIND_VIEW
        
    Limitations:
        Specifically looks for DISPLAYS edges pointing to the query target.
    """
    rule_type = RankingRuleType.VIEW
    supported_query_types = [QueryType.FIND_VIEW]

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        results = []
        if query.query_type in self.supported_query_types:
            for edge in graph.find_edges_by_type(RelationshipType.DISPLAYS):
                if edge.target_id == query.target_node:
                    source_node = graph.get_node(edge.source_id)
                    if source_node.node_type == NodeType.VIEW:
                        results.append(
                            RankingResult(
                                query_id=query.query_id,
                                node_id=source_node.node_id,
                                score=RankingScore.VIEW,
                                matched_rule=self.rule_type,
                                reason=RankingReason.VIEW_REFERENCE,
                                metadata=freeze_metadata({
                                    "module": source_node.module,
                                    "language": source_node.language.value,
                                    "relative_path": source_node.relative_path,
                                    "start_line": 0,
                                    "matched_relationship": edge.relationship_type.value,
                                    "displays": query.target_symbol
                                })
                            )
                        )
        return results
