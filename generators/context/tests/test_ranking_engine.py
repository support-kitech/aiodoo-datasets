import unittest
import logging

from generators.context.analysis.graph import ContextGraph
from generators.context.generation.query import Query
from generators.context.generation.enums import QueryType, QueryIntent
from generators.context.ranking.enums import (
    RankingRuleType,
    RankingScore,
    RankingReason,
)
from generators.context.ranking.result import RankingResult
from generators.context.ranking.base import BaseRankingRule
from generators.context.ranking.registry import REGISTERED_RANKING_RULES
from generators.context.ranking.ranking_engine import RankingEngine
from generators.context.ranking.utils import freeze_metadata


class MockCrashingRule(BaseRankingRule):
    rule_type = RankingRuleType.DEFINITION
    supported_query_types = [QueryType.FIND_MODEL]

    def rank(self, query, graph):
        raise ValueError("Intentional crash")


class MockMultiRule1(BaseRankingRule):
    rule_type = RankingRuleType.DEFINITION
    supported_query_types = [QueryType.FIND_MODEL]

    def rank(self, query, graph):
        return [
            RankingResult(
                "q1",
                "node_a",
                RankingScore.DEFINITION,
                self.rule_type,
                RankingReason.DIRECT_DEFINITION,
                metadata=freeze_metadata({"start_line": 10}),
            )
        ]


class MockMultiRule2(BaseRankingRule):
    rule_type = RankingRuleType.INHERITANCE
    supported_query_types = [QueryType.FIND_MODEL]

    def rank(self, query, graph):
        # Same node, different score
        return [
            RankingResult(
                "q1",
                "node_a",
                RankingScore.INHERITANCE,
                self.rule_type,
                RankingReason.MODEL_INHERITANCE,
                metadata=freeze_metadata({"start_line": 10}),
            )
        ]


class MockMultiRuleAction(BaseRankingRule):
    rule_type = RankingRuleType.ACTION
    supported_query_types = [QueryType.FIND_MODEL]

    def rank(self, query, graph):
        # Same node, action score
        return [
            RankingResult(
                "q1",
                "node_a",
                RankingScore.ACTION,
                self.rule_type,
                RankingReason.ACTION_REFERENCE,
                metadata=freeze_metadata({"start_line": 10}),
            )
        ]


class MockTieRule1(BaseRankingRule):
    rule_type = RankingRuleType.DEFINITION
    supported_query_types = [QueryType.FIND_MODEL]

    def rank(self, query, graph):
        # Tie break on node_id -> relative_path -> start_line
        # Node Z has score 50, Node A has score 50 (Using raw numbers here just to test tie-breaking logic regardless of enum)
        return [
            RankingResult(
                "q1",
                "node_z",
                RankingScore.ACTION,
                self.rule_type,
                RankingReason.DIRECT_DEFINITION,
                metadata=freeze_metadata({"relative_path": "b", "start_line": 20}),
            ),
            RankingResult(
                "q1",
                "node_a",
                RankingScore.ACTION,
                self.rule_type,
                RankingReason.DIRECT_DEFINITION,
                metadata=freeze_metadata({"relative_path": "a", "start_line": 10}),
            ),
        ]


class TestRankingEngine(unittest.TestCase):
    def setUp(self) -> None:
        logging.getLogger("generators.context.ranking.ranking_engine").setLevel(
            logging.CRITICAL
        )
        self.graph = ContextGraph()

    def test_registry_validation(self) -> None:
        self.assertIsInstance(REGISTERED_RANKING_RULES, tuple)
        self.assertEqual(len(REGISTERED_RANKING_RULES), len(set(REGISTERED_RANKING_RULES)))

        rule_types = set()
        for rule_cls in REGISTERED_RANKING_RULES:
            self.assertTrue(issubclass(rule_cls, BaseRankingRule))
            r_type = getattr(rule_cls, "rule_type", None)
            self.assertIsNotNone(r_type)
            self.assertNotIn(r_type, rule_types)
            rule_types.add(r_type)

    def test_registration_order(self) -> None:
        engine = RankingEngine()
        rule_names = [r.__class__.__name__ for r in engine.rules]
        expected = [
            "ActionRule",
            "DefinitionRule",
            "DependencyRule",
            "InheritanceRule",
            "SecurityRule",
            "ViewRule",
        ]
        self.assertEqual(rule_names, expected)

    def test_max_aggregation_and_deduplication(self) -> None:
        engine = RankingEngine()
        engine.rules = [MockMultiRule1(), MockMultiRule2(), MockMultiRuleAction()]
        query = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, "target_node", "symbol", "NL")

        results = engine.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, "node_a")
        # Ensure max aggregation worked: 100 > 90 > 60
        self.assertEqual(results[0].score, RankingScore.DEFINITION)
        self.assertEqual(results[0].matched_rule, RankingRuleType.DEFINITION)

    def test_tie_breaking_ordering(self) -> None:
        engine = RankingEngine()
        engine.rules = [MockTieRule1()]
        query = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, "target", "symbol", "NL")

        results = engine.rank(query, self.graph)
        self.assertEqual(len(results), 2)
        # Node A should come before Node Z due to relative_path / start_line / ID sorting fallback when scores tie
        self.assertEqual(results[0].node_id, "node_a")
        self.assertEqual(results[1].node_id, "node_z")

    def test_fault_tolerance(self) -> None:
        engine = RankingEngine()
        engine.rules = [MockCrashingRule(), MockMultiRule1()]
        query = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, "target", "symbol", "NL")

        results = engine.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, "node_a")

    def test_identical_executions(self) -> None:
        engine = RankingEngine()
        engine.rules = [MockTieRule1(), MockMultiRule1(), MockMultiRule2()]
        query = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, "target", "symbol", "NL")

        run1 = engine.rank(query, self.graph)
        run2 = engine.rank(query, self.graph)
        self.assertEqual(run1, run2)


if __name__ == "__main__":
    unittest.main()
