import unittest
from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.node import ExecutionNode
from generators.execution.graph.edge import ExecutionEdge
from generators.execution.graph.enums import NodeType, EdgeType
from generators.execution.validation.graph_validator import GraphValidator
from generators.execution.validation.node_validator import NodeValidator
from generators.execution.validation.edge_validator import EdgeValidator


class TestGraphValidator(unittest.TestCase):
    def test_valid_graph(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p")
        n2 = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="p")
        e = ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n1, n2), edges=(e,))

        result = GraphValidator.validate(graph)
        self.assertTrue(result.success)
        self.assertEqual(len(result.violations), 0)

    def test_duplicate_node_id(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p1")
        n2 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p2")
        graph = ExecutionGraph(nodes=(n1, n2), edges=())

        result = NodeValidator.validate(graph)
        self.assertFalse(result.success)
        self.assertTrue(any("Duplicate" in v for v in result.violations))

    def test_self_loop(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p")
        e = ExecutionEdge(source_id="a", target_id="a", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n1,), edges=(e,))

        result = EdgeValidator.validate(graph)
        self.assertFalse(result.success)
        self.assertTrue(any("Self-loop" in v for v in result.violations))

    def test_dangling_edge(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p")
        e = ExecutionEdge(source_id="a", target_id="z", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n1,), edges=(e,))

        result = EdgeValidator.validate(graph)
        self.assertFalse(result.success)
        self.assertTrue(any("non-existent" in v for v in result.violations))

    def test_none_payload(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload=None)
        graph = ExecutionGraph(nodes=(n1,), edges=())

        result = NodeValidator.validate(graph)
        self.assertFalse(result.success)


if __name__ == "__main__":
    unittest.main()
