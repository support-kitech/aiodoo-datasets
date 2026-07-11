"""Action Ranking Rule."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.analysis.graph.enums import RelationshipType, NodeType
from aiodoo_datasets.generators.context.generation.query import Query, QueryType
from aiodoo_datasets.generators.context.ranking.enums import (
    RankingRuleType,
    RankingScore,
    RankingReason,
)
from aiodoo_datasets.generators.context.ranking.result import RankingResult
from aiodoo_datasets.generators.context.ranking.base import BaseRankingRule
from aiodoo_datasets.generators.context.ranking.utils import freeze_metadata


class ActionRule(BaseRankingRule):
    """
    Ranks UI Actions and Menus.

    Engineering Purpose:
        Identifies Actions or Menus that open or trigger a target.
        Scores (60).

    Supported Queries:
        FIND_ACTION
        FIND_MENU

    Limitations:
        Specifically looks for TRIGGERS edges.
    """

    rule_type = RankingRuleType.ACTION
    supported_query_types = [QueryType.FIND_ACTION, QueryType.FIND_MENU]

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        results = []
        if query.query_type in self.supported_query_types:
            for edge in graph.find_edges_by_type(RelationshipType.TRIGGERS):
                if edge.target_id == query.target_node:
                    source_node = graph.get_node(edge.source_id)
                    # For FIND_ACTION query, we look for ACTION nodes
                    # For FIND_MENU query, we look for MENU nodes
                    if (
                        query.query_type == QueryType.FIND_ACTION
                        and source_node.node_type == NodeType.ACTION
                    ):
                        results.append(self._build_result(query, source_node, edge))
                    elif (
                        query.query_type == QueryType.FIND_MENU
                        and source_node.node_type == NodeType.MENU
                    ):
                        results.append(self._build_result(query, source_node, edge))
        return results

    def _build_result(self, query: Query, node, edge) -> RankingResult:
        return RankingResult(
            query_id=query.query_id,
            node_id=node.node_id,
            score=RankingScore.ACTION,
            matched_rule=self.rule_type,
            reason=RankingReason.ACTION_REFERENCE,
            metadata=freeze_metadata(
                {
                    "module": node.module,
                    "language": node.language.value,
                    "relative_path": node.relative_path,
                    "start_line": 0,
                    "matched_relationship": edge.relationship_type.value,
                    "triggers": query.target_symbol,
                }
            ),
        )
