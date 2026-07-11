import unittest
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.edge import ExecutionEdge
from aiodoo_datasets.generators.execution.graph.enums import NodeType, EdgeType
from aiodoo_datasets.generators.execution.graph.detector import CycleDetector
from aiodoo_datasets.generators.execution.graph.exceptions import CycleDetectedError


class TestCycleDetector(unittest.TestCase):
    def test_acyclic(self):
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p1")
        n2 = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="p2")
        e = ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n1, n2), edges=(e,))

        result = CycleDetector.detect(graph)
        self.assertEqual(result, ())

    def test_simple_cycle(self):
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p1")
        n2 = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="p2")
        e1 = ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY)
        e2 = ExecutionEdge(source_id="b", target_id="a", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n1, n2), edges=(e1, e2))

        with self.assertRaises(CycleDetectedError) as ctx:
            CycleDetector.detect(graph)
        self.assertTrue(len(ctx.exception.cycles) > 0)

    def test_self_loop(self):
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p1")
        e = ExecutionEdge(source_id="a", target_id="a", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n1,), edges=(e,))

        with self.assertRaises(CycleDetectedError):
            CycleDetector.detect(graph)

    def test_complex_multi_path(self):
        nodes = tuple(ExecutionNode(node_id=c, node_type=NodeType.STEP, payload=c) for c in "abcd")
        edges = (
            ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="b", target_id="c", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="c", target_id="d", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="d", target_id="b", edge_type=EdgeType.DEPENDENCY),
        )
        graph = ExecutionGraph(nodes=nodes, edges=edges)

        with self.assertRaises(CycleDetectedError):
            CycleDetector.detect(graph)


if __name__ == "__main__":
    unittest.main()
