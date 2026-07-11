import unittest
from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.node import ExecutionNode
from generators.execution.graph.edge import ExecutionEdge
from generators.execution.graph.enums import NodeType, EdgeType, TraversalStrategy
from generators.execution.graph.traversal import GraphTraversal


class TestGraphTraversal(unittest.TestCase):
    def _make_graph(self):
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="a")
        n2 = ExecutionNode(node_id="b", node_type=NodeType.STEP, payload="b")
        n3 = ExecutionNode(node_id="c", node_type=NodeType.STEP, payload="c")
        e1 = ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY)
        e2 = ExecutionEdge(source_id="b", target_id="c", edge_type=EdgeType.DEPENDENCY)
        return ExecutionGraph(nodes=(n1, n2, n3), edges=(e1, e2))

    def test_dfs(self) -> None:
        graph = self._make_graph()
        result = GraphTraversal.traverse(graph, TraversalStrategy.DFS)
        self.assertTrue(result.success)
        self.assertEqual(result.strategy, TraversalStrategy.DFS)
        ids = [n.node_id for n in result.nodes]
        self.assertEqual(ids[0], "a")
        self.assertEqual(len(ids), 3)

    def test_bfs(self) -> None:
        graph = self._make_graph()
        result = GraphTraversal.traverse(graph, TraversalStrategy.BFS)
        self.assertTrue(result.success)
        ids = [n.node_id for n in result.nodes]
        self.assertEqual(ids, ["a", "b", "c"])

    def test_reverse(self) -> None:
        graph = self._make_graph()
        result = GraphTraversal.traverse(graph, TraversalStrategy.REVERSE)
        self.assertTrue(result.success)
        ids = [n.node_id for n in result.nodes]
        self.assertEqual(ids[0], "c")

    def test_dependency(self) -> None:
        graph = self._make_graph()
        result = GraphTraversal.traverse(graph, TraversalStrategy.DEPENDENCY)
        self.assertTrue(result.success)
        self.assertEqual(len(result.nodes), 3)

    def test_no_mutation(self) -> None:
        graph = self._make_graph()
        nodes_before = graph.nodes
        edges_before = graph.edges
        GraphTraversal.traverse(graph, TraversalStrategy.DFS)
        self.assertEqual(graph.nodes, nodes_before)
        self.assertEqual(graph.edges, edges_before)


if __name__ == "__main__":
    unittest.main()
