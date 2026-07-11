import unittest

from generators.context.analysis.graph import (
    ContextNode,
    ContextEdge,
    ContextGraph,
    NodeType,
    LanguageType,
    RelationshipType,
)


class TestContextNode(unittest.TestCase):
    def test_node_creation_and_deterministic_id(self) -> None:
        node1 = ContextNode(
            name="sale.order",
            module="sale",
            relative_path="models/sale_order.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
            start_line=10,
            end_line=50,
        )

        node2 = ContextNode(
            name="sale.order",
            module="sale",
            relative_path="models/sale_order.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
            start_line=10,
            end_line=100,  # Different end line shouldn't affect ID based on our spec
        )

        node3 = ContextNode(
            name="sale.order",
            module="sale",
            relative_path="models/sale_order.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
            start_line=11,  # Different start line should affect ID
            end_line=50,
        )

        self.assertEqual(node1.node_id, node2.node_id)
        self.assertNotEqual(node1.node_id, node3.node_id)
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertEqual(hash(node1), hash(node2))

    def test_node_serialization(self) -> None:
        node = ContextNode(
            name="sale.order",
            module="sale",
            relative_path="models/sale_order.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
            start_line=10,
            metadata={"framework": "odoo"},
        )

        node_dict = node.to_dict()
        node_reconstructed = ContextNode.from_dict(node_dict)

        self.assertEqual(node.node_id, node_reconstructed.node_id)
        self.assertEqual(node, node_reconstructed)
        self.assertEqual(node.metadata, node_reconstructed.metadata)


class TestContextEdge(unittest.TestCase):
    def test_edge_creation_and_deterministic_id(self) -> None:
        edge1 = ContextEdge(
            source_id="id1", target_id="id2", relationship_type=RelationshipType.CONTAINS
        )

        edge2 = ContextEdge(
            source_id="id1", target_id="id2", relationship_type=RelationshipType.CONTAINS
        )

        edge3 = ContextEdge(
            source_id="id1", target_id="id2", relationship_type=RelationshipType.INHERITS
        )

        self.assertEqual(edge1.edge_id, edge2.edge_id)
        self.assertNotEqual(edge1.edge_id, edge3.edge_id)
        self.assertEqual(edge1, edge2)
        self.assertNotEqual(edge1, edge3)

    def test_edge_serialization(self) -> None:
        edge = ContextEdge(
            source_id="id1",
            target_id="id2",
            relationship_type=RelationshipType.CONTAINS,
            metadata={"weight": 1.0},
        )

        edge_dict = edge.to_dict()
        edge_reconstructed = ContextEdge.from_dict(edge_dict)

        self.assertEqual(edge.edge_id, edge_reconstructed.edge_id)
        self.assertEqual(edge, edge_reconstructed)
        self.assertEqual(edge.metadata, edge_reconstructed.metadata)


class TestContextGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = ContextGraph()
        self.node1 = ContextNode(
            name="node1",
            module="base",
            relative_path="a.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
            start_line=1,
        )
        self.node2 = ContextNode(
            name="node2",
            module="base",
            relative_path="b.py",
            node_type=NodeType.FIELD,
            language=LanguageType.PYTHON,
            start_line=2,
        )
        self.edge1 = ContextEdge(
            source_id=self.node1.node_id,
            target_id=self.node2.node_id,
            relationship_type=RelationshipType.CONTAINS,
        )

    def test_graph_add_and_retrieve(self) -> None:
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)

        self.assertTrue(self.graph.contains_node(self.node1.node_id))
        self.assertTrue(self.graph.contains_edge(self.edge1.edge_id))
        self.assertEqual(self.graph.node_count(), 2)
        self.assertEqual(self.graph.edge_count(), 1)

        retrieved_node = self.graph.get_node(self.node1.node_id)
        self.assertEqual(self.node1, retrieved_node)

        outgoing = self.graph.get_outgoing_edges(self.node1.node_id)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0], self.edge1)

        incoming = self.graph.get_incoming_edges(self.node2.node_id)
        self.assertEqual(len(incoming), 1)
        self.assertEqual(incoming[0], self.edge1)

        neighbors_n1 = self.graph.get_neighbors(self.node1.node_id)
        neighbors_n2 = self.graph.get_neighbors(self.node2.node_id)

        self.assertEqual(len(neighbors_n1), 1)
        self.assertEqual(neighbors_n1[0], self.edge1)

        self.assertEqual(len(neighbors_n2), 1)
        self.assertEqual(neighbors_n2[0], self.edge1)

    def test_duplicate_prevention(self):
        # Duplicate nodes are ignored.
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node1)

        self.assertEqual(self.graph.node_count(), 1)

        self.graph.add_node(self.node2)

        # Duplicate edges are also ignored.
        self.graph.add_edge(self.edge1)
        self.graph.add_edge(self.edge1)

        self.assertEqual(self.graph.edge_count(), 1)

        def test_missing_node_edge_prevention(self) -> None:
            # Adding edge before adding nodes
            with self.assertRaises(ValueError):
                self.graph.add_edge(self.edge1)

    def test_deterministic_ordering(self) -> None:
        # Node ordering depends on relative_path, then start_line
        n_z = ContextNode(
            name="z",
            module="base",
            relative_path="z.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
        )
        n_a = ContextNode(
            name="a",
            module="base",
            relative_path="a.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
        )
        n_m = ContextNode(
            name="m",
            module="base",
            relative_path="m.py",
            node_type=NodeType.MODEL,
            language=LanguageType.PYTHON,
        )

        self.graph.add_node(n_z)
        self.graph.add_node(n_a)
        self.graph.add_node(n_m)

        nodes = self.graph.get_nodes()
        self.assertEqual(nodes[0].relative_path, "a.py")
        self.assertEqual(nodes[1].relative_path, "m.py")
        self.assertEqual(nodes[2].relative_path, "z.py")

    def test_graph_serialization(self) -> None:
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)

        graph_dict = self.graph.to_dict()
        reconstructed_graph = ContextGraph.from_dict(graph_dict)

        self.assertEqual(reconstructed_graph.node_count(), 2)
        self.assertEqual(reconstructed_graph.edge_count(), 1)
        self.assertTrue(reconstructed_graph.contains_node(self.node1.node_id))
        self.assertTrue(reconstructed_graph.contains_edge(self.edge1.edge_id))


if __name__ == "__main__":
    unittest.main()
