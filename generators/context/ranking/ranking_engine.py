"""Orchestrates query evaluation and artifact ranking."""

import logging

from generators.context.analysis.graph.graph import ContextGraph
from generators.context.generation.query import Query
from generators.context.ranking.result import RankingResult
from generators.context.ranking.registry import REGISTERED_RANKING_RULES

logger = logging.getLogger(__name__)


class RankingEngine:
    """
    Orchestrates the execution of statically registered Ranking Rules.

    Responsibilities:
    - Executes ranking rules applicable to a specific Query.
    - Aggregates scores (using max() to prevent artificial inflation).
    - Deduplicates identical node targets.
    - Returns deterministically sorted RankingResults.
    - Provides fault tolerance for failing plugins.
    """

    def __init__(self) -> None:
        # Register rules statically and ensure deterministic alphabetical sorting.
        self.rules = sorted(
            [rule_cls() for rule_cls in REGISTERED_RANKING_RULES],
            key=lambda r: r.__class__.__name__,
        )

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        """
        Execute all applicable ranking rules for the given query.

        Args:
            query: The engineering query to rank context against.
            graph: A fully populated, read-only ContextGraph.

        Returns:
            A deterministically sorted list of unique RankingResult objects.
        """
        # Dictionary to track best result per node_id: {node_id: RankingResult}
        best_results_by_node = {}

        for rule in self.rules:
            # Skip rule if it doesn't support this query type
            if query.query_type not in rule.supported_query_types:
                continue

            try:
                results = rule.rank(query, graph)

                for r in results:
                    node_id = r.node_id
                    if node_id not in best_results_by_node:
                        best_results_by_node[node_id] = r
                    else:
                        # Aggregation Strategy: Use max() score to prevent artificial boosting.
                        existing_result = best_results_by_node[node_id]
                        if r.score > existing_result.score:
                            best_results_by_node[node_id] = r
                        elif r.score == existing_result.score:
                            # In case of tie on score between two rules targeting the same node,
                            # ensure determinism by picking the one with lower matched_rule string value.
                            # Usually this shouldn't happen for the same node, but just in case:
                            if r.matched_rule.value < existing_result.matched_rule.value:
                                best_results_by_node[node_id] = r

            except Exception as e:
                rule_type = getattr(rule, "rule_type", "Unknown")
                if hasattr(rule_type, "value"):
                    rule_type = rule_type.value

                module = getattr(e, "module", "Unknown")
                node_id = getattr(e, "node_id", "Unknown")

                logger.exception(
                    "Ranking Rule Failed\n"
                    "Rule: %s\n"
                    "Query Type: %s\n"
                    "Query ID: %s\n"
                    "Node ID: %s\n"
                    "Module: %s",
                    rule.__class__.__name__,
                    query.query_type.value,
                    query.query_id,
                    node_id,
                    module,
                )

        # Deterministically sort all best results before returning
        return sorted(list(best_results_by_node.values()))
