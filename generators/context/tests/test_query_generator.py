import unittest
import logging

from aiodoo_datasets.generators.context.analysis.graph import ContextGraph, NodeType
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.generation.query_generator import QueryGenerator
from aiodoo_datasets.generators.context.generation.registry import REGISTERED_QUERY_PLUGINS
from aiodoo_datasets.generators.context.generation.queries.base import BaseContextQuery


class MockCrashingPlugin(BaseContextQuery):
    query_type = QueryType.FIND_MODEL
    supported_node_types = [NodeType.MODEL]

    def generate(self, graph: ContextGraph) -> list[Query]:
        raise ValueError("Intentional crash for fault tolerance test")


class MockDuplicatePlugin(BaseContextQuery):
    query_type = QueryType.FIND_MODEL
    supported_node_types = [NodeType.MODEL]

    def generate(self, graph: ContextGraph) -> list[Query]:
        # Yield the exact same query twice
        q1 = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, "node_1", "symbol", "NL")
        q2 = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, "node_1", "symbol", "NL")
        return [q1, q2]


class TestQueryGenerator(unittest.TestCase):
    def setUp(self) -> None:
        logging.getLogger("aiodoo_datasets.generators.context.generation.query_generator").setLevel(
            logging.CRITICAL
        )
        self.graph = ContextGraph()

    def test_registry_validation(self) -> None:
        self.assertIsInstance(REGISTERED_QUERY_PLUGINS, tuple)
        # Ensure no duplicate plugins
        self.assertEqual(len(REGISTERED_QUERY_PLUGINS), len(set(REGISTERED_QUERY_PLUGINS)))

        query_types = set()
        for plugin_cls in REGISTERED_QUERY_PLUGINS:
            # Ensure every plugin subclasses BaseContextQuery
            self.assertTrue(issubclass(plugin_cls, BaseContextQuery))
            # Ensure every plugin exposes a unique QueryType
            q_type = getattr(plugin_cls, "query_type", None)
            self.assertIsNotNone(q_type)
            self.assertNotIn(q_type, query_types)
            query_types.add(q_type)

    def test_registration_order(self) -> None:
        generator = QueryGenerator()
        plugin_names = [p.__class__.__name__ for p in generator.plugins]
        expected = [
            "FindActionQuery",
            "FindComputeQuery",
            "FindDependencyQuery",
            "FindFieldQuery",
            "FindMenuQuery",
            "FindModelQuery",
            "FindSecurityQuery",
            "FindViewQuery",
        ]
        self.assertEqual(plugin_names, expected)

    def test_fault_tolerance(self) -> None:
        generator = QueryGenerator()
        generator.plugins = [MockCrashingPlugin(), MockDuplicatePlugin()]

        # Should not raise exception, crashing plugin is bypassed
        queries = generator.generate_queries(self.graph)

        # Duplicate plugin yields 2 queries but duplicate removal keeps 1
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].target_symbol, "symbol")

    def test_duplicate_prevention_and_determinism(self) -> None:
        generator = QueryGenerator()
        generator.plugins = [MockDuplicatePlugin()]

        queries1 = generator.generate_queries(self.graph)
        self.assertEqual(len(queries1), 1)

        # Run twice to ensure deterministic exact output
        queries2 = generator.generate_queries(self.graph)
        self.assertEqual(queries1, queries2)

        # Check dictionary serialization
        self.assertEqual(queries1[0].to_dict(), queries2[0].to_dict())


if __name__ == "__main__":
    unittest.main()
