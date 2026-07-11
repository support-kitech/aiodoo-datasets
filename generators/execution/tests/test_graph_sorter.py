import unittest
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.edge import ExecutionEdge
from aiodoo_datasets.generators.execution.graph.enums import NodeType, EdgeType
from aiodoo_datasets.generators.execution.graph.sorter import TopologicalSorter


class TestGraphSorter(unittest.TestCase):
    def test_linear_sort(self):
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p1")
        n2 = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="p2")
        n3 = ExecutionNode(node_id="c", node_type=NodeType.STEP, payload="p3")
        e1 = ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY)
        e2 = ExecutionEdge(source_id="b", target_id="c", edge_type=EdgeType.DEPENDENCY)
        graph = ExecutionGraph(nodes=(n3, n1, n2), edges=(e1, e2))

        result = TopologicalSorter.sort(graph)
        self.assertTrue(result.success)
        self.assertFalse(result.has_cycles)
        ids = [n.node_id for n in result.sorted_nodes]
        self.assertEqual(ids, ["a", "b", "c"])

    def test_deterministic_parallel(self):
        nodes = tuple(ExecutionNode(node_id=c, node_type=NodeType.STEP, payload=c) for c in "dcba")
        graph = ExecutionGraph(nodes=nodes, edges=())

        r1 = TopologicalSorter.sort(graph)
        r2 = TopologicalSorter.sort(graph)
        ids1 = [n.node_id for n in r1.sorted_nodes]
        ids2 = [n.node_id for n in r2.sorted_nodes]
        self.assertEqual(ids1, ids2)
        # Secondary alphanumeric ordering
        self.assertEqual(ids1, ["a", "b", "c", "d"])

    def test_diamond(self):
        na = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="a")
        nb = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="b")
        nc = ExecutionNode(node_id="c", node_type=NodeType.STEP, payload="c")
        nd = ExecutionNode(node_id="d", node_type=NodeType.STEP, payload="d")
        edges = (
            ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="a", target_id="c", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="b", target_id="d", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="c", target_id="d", edge_type=EdgeType.DEPENDENCY),
        )
        graph = ExecutionGraph(nodes=(na, nb, nc, nd), edges=edges)

        result = TopologicalSorter.sort(graph)
        ids = [n.node_id for n in result.sorted_nodes]
        # a must come first, d must come last, b and c in between (alpha order)
        self.assertEqual(ids[0], "a")
        self.assertEqual(ids[-1], "d")
        self.assertIn("b", ids[1:3])
        self.assertIn("c", ids[1:3])


if __name__ == "__main__":
    unittest.main()
