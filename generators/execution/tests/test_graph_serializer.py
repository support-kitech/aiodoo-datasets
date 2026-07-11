import unittest
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.edge import ExecutionEdge
from aiodoo_datasets.generators.execution.graph.enums import NodeType, EdgeType
from aiodoo_datasets.generators.execution.graph.serializer import GraphSerializer


class TestGraphSerializer(unittest.TestCase):
    def test_deterministic(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p")
        n2 = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="p")
        e = ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n2, n1), edges=(e,))

        s1 = GraphSerializer.serialize(graph)
        s2 = GraphSerializer.serialize(graph)
        self.assertEqual(s1, s2)

    def test_identical_graphs(self) -> None:
        """Two graphs with the same structure must produce identical serialization."""
        g1 = ExecutionGraph(
            nodes=(
                ExecutionNode(node_id="x", node_type=NodeType.STEP, payload="x"),
                ExecutionNode(node_id="y", node_type=NodeType.STEP, payload="y"),
            ),
            edges=(ExecutionEdge(source_id="x", target_id="y", edge_type=EdgeType.SEQUENCE),),
        )
        g2 = ExecutionGraph(
            nodes=(
                ExecutionNode(node_id="y", node_type=NodeType.STEP, payload="y"),
                ExecutionNode(node_id="x", node_type=NodeType.STEP, payload="x"),
            ),
            edges=(ExecutionEdge(source_id="x", target_id="y", edge_type=EdgeType.SEQUENCE),),
        )
        self.assertEqual(GraphSerializer.serialize(g1), GraphSerializer.serialize(g2))

    def test_empty_graph(self) -> None:
        graph = ExecutionGraph()
        result = GraphSerializer.serialize(graph)
        self.assertIn('"edges":[]', result)
        self.assertIn('"nodes":[]', result)


if __name__ == "__main__":
    unittest.main()
