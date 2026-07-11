"""Inheritance Ranking Rule."""

from generators.context.analysis.graph.graph import ContextGraph
from generators.context.analysis.graph.enums import RelationshipType
from generators.context.generation.query import Query, QueryType
from generators.context.ranking.enums import (
    RankingRuleType,
    RankingScore,
    RankingReason,
)
from generators.context.ranking.result import RankingResult
from generators.context.ranking.base import BaseRankingRule
from generators.context.ranking.utils import freeze_metadata


class InheritanceRule(BaseRankingRule):  # type: ignore[misc]
    """
    Ranks inherited implementations.

    Engineering Purpose:
        Identifies nodes that inherit from the query target.
        Scores high (90) because inherited implementations often contain relevant extensions.

    Supported Queries:
        FIND_MODEL

    Limitations:
        Only traverses one level of INHERITS edges explicitly.
    """

    rule_type = RankingRuleType.INHERITANCE
    supported_query_types = [QueryType.FIND_MODEL]

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        results = []
        if query.query_type in self.supported_query_types:
            # We are looking for nodes that INHERIT from the target node
            # So the target node is the target_id of an INHERITS edge
            for edge in graph.find_edges_by_type(RelationshipType.INHERITS):
                if edge.target_id == query.target_node:
                    source_node = graph.get_node(edge.source_id)
                    results.append(
                        RankingResult(
                            query_id=query.query_id,
                            node_id=source_node.node_id,
                            score=RankingScore.INHERITANCE,
                            matched_rule=self.rule_type,
                            reason=RankingReason.MODEL_INHERITANCE,
                            metadata=freeze_metadata(
                                {
                                    "module": source_node.module,
                                    "language": source_node.language.value,
                                    "relative_path": source_node.relative_path,
                                    "start_line": 0,
                                    "matched_relationship": edge.relationship_type.value,
                                    "inherited_from": query.target_symbol,
                                }
                            ),
                        )
                    )
        return results
