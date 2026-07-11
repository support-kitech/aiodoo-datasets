import unittest
import logging

from aiodoo_datasets.generators.context.analysis.graph import (
    ContextNode,
    ContextEdge,
    ContextGraph,
    NodeType,
    LanguageType,
    RelationshipType,
)
from aiodoo_datasets.generators.context.analysis.graph_builder import GraphBuilder
from aiodoo_datasets.generators.context.analysis.relationships.base import BaseRelationshipExtractor
from aiodoo_datasets.generators.context.analysis.knowledge import ContextKnowledge


class MockCrashingExtractor(BaseRelationshipExtractor):
    relation_type = RelationshipType.CONTAINS
    supported_languages = [LanguageType.PYTHON]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        raise ValueError("Intentional crash for fault tolerance test")


class MockSuccessExtractor(BaseRelationshipExtractor):
    relation_type = RelationshipType.CONTAINS
    supported_languages = [LanguageType.PYTHON]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        nodes = graph.get_nodes()
        if len(nodes) >= 2:
            return [
                ContextEdge(
                    source_id=nodes[0].node_id,
                    target_id=nodes[1].node_id,
                    relationship_type=RelationshipType.CONTAINS,
                )
            ]
        return []


class MockMissingNodeExtractor(BaseRelationshipExtractor):
    relation_type = RelationshipType.CONTAINS
    supported_languages = [LanguageType.PYTHON]

    def extract(self, graph: ContextGraph, knowledge: ContextKnowledge) -> list[ContextEdge]:
        return [
            ContextEdge(
                source_id="fake_source_123",
                target_id="fake_target_456",
                relationship_type=RelationshipType.CONTAINS,
            )
        ]


class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        # Disable logging for the duration of the tests to keep console clean
        logging.getLogger("aiodoo_datasets.generators.context.analysis.graph_builder").setLevel(
            logging.CRITICAL
        )

        self.graph = ContextGraph()
        self.node1 = ContextNode(
            "model_a", "base", "a.py", NodeType.MODEL, LanguageType.PYTHON, start_line=1
        )
        self.node2 = ContextNode(
            "field_b", "base", "a.py", NodeType.FIELD, LanguageType.PYTHON, start_line=5
        )
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.knowledge = ContextKnowledge(module_name="test_module")

    def test_registration_order(self):
        builder = GraphBuilder()
        # Ensure exact alphabetical determinism
        extractor_names = [e.__class__.__name__ for e in builder.extractors]
        expected = [
            "ComputesRelationship",
            "ContainsRelationship",
            "DisplaysRelationship",
            "InheritsRelationship",
            "TriggersRelationship",
        ]
        self.assertEqual(extractor_names, expected)

    def test_fault_tolerance(self):
        builder = GraphBuilder()
        # Inject our mock crashing extractor
        builder.extractors.append(MockCrashingExtractor())
        builder.extractors.append(MockSuccessExtractor())

        # This should not raise an exception, the crashing extractor should be skipped
        builder.build_relationships(self.graph, self.knowledge)

        # The success extractor should still have successfully added 1 edge
        self.assertEqual(self.graph.edge_count(), 1)

    def test_invalid_node_rejection(self):
        builder = GraphBuilder()
        builder.extractors = [MockMissingNodeExtractor()]

        # Missing nodes should log a warning but be safely rejected
        builder.build_relationships(self.graph, self.knowledge)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_duplicate_prevention_and_determinism(self):
        builder = GraphBuilder()
        # Inject the success extractor multiple times to simulate duplicate edge proposals
        builder.extractors = [MockSuccessExtractor(), MockSuccessExtractor()]

        builder.build_relationships(self.graph, self.knowledge)

        # Duplicate edges should be safely ignored
        self.assertEqual(self.graph.edge_count(), 1)

        # Test double-run determinism
        graph_dict_1 = self.graph.to_dict()

        # Second run should result in exact same state
        builder.build_relationships(self.graph, self.knowledge)
        graph_dict_2 = self.graph.to_dict()

        self.assertEqual(graph_dict_1, graph_dict_2)


if __name__ == "__main__":
    unittest.main()
