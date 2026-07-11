"""Base interface for Ranking Rules."""

from generators.context.analysis.graph.graph import ContextGraph
from generators.context.generation.query import Query, QueryType
from generators.context.ranking.enums import RankingRuleType
from generators.context.ranking.result import RankingResult


class BaseRankingRule:
    """
    Base interface for all ranking rules.

    Responsibilities:
    - Declares the rule_type and supported_query_types.
    - Inspects the graph to find nodes relevant to a Query.
    - Deterministically generates RankingResult objects.
    - Graph and Query must be treated as completely read-only.
    """

    rule_type: RankingRuleType
    supported_query_types: list[QueryType]

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        """
        Generates RankingResult objects based on the given query.

        Args:
            query: The originating engineering query.
            graph: The fully populated ContextGraph.

        Returns:
            A list of new RankingResult objects.
        """
        raise NotImplementedError("Ranking rules must implement rank()")
