import unittest
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.edge import ExecutionEdge
from aiodoo_datasets.generators.execution.graph.enums import NodeType, EdgeType
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics


class TestGraphStatistics(unittest.TestCase):
    def _compute(self, graph: ExecutionGraph) -> GraphStatistics:
        """Compute all graph statistics."""
        stats = GraphStatistics()
        stats.node_count = len(graph.nodes)
        stats.edge_count = len(graph.edges)
        stats.root_count = len(graph.roots)
        stats.leaf_count = len(graph.leaves)

        # Isolated nodes: no edges at all
        connected = set()
        for e in graph.edges:
            connected.add(e.source_id)
            connected.add(e.target_id)
        stats.isolated_nodes = sum(1 for n in graph.nodes if n.node_id not in connected)

        # Compute depth via BFS from roots
        adjacency = {n.node_id: [] for n in graph.nodes}
        for e in graph.edges:
            if e.source_id in adjacency:
                adjacency[e.source_id].append(e.target_id)

        max_depth = 0
        width_per_level: dict[int, int] = {}
        for root in graph.roots:
            queue = [(root.node_id, 0)]
            visited = {root.node_id}
            while queue:
                nid, d = queue.pop(0)
                max_depth = max(max_depth, d)
                width_per_level[d] = width_per_level.get(d, 0) + 1
                for neighbor in adjacency.get(nid, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, d + 1))

        stats.graph_depth = max_depth
        stats.graph_width = max(width_per_level.values()) if width_per_level else 0
        stats.longest_path = max_depth
        stats.parallel_branches = max(0, stats.graph_width - 1)

        return stats

    def test_linear_graph(self) -> None:
        nodes = tuple(ExecutionNode(node_id=c, node_type=NodeType.STEP, payload=c) for c in "abc")
        edges = (
            ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="b", target_id="c", edge_type=EdgeType.DEPENDENCY),
        )
        graph = ExecutionGraph(nodes=nodes, edges=edges)
        stats = self._compute(graph)

        self.assertEqual(stats.node_count, 3)
        self.assertEqual(stats.edge_count, 2)
        self.assertEqual(stats.root_count, 1)
        self.assertEqual(stats.leaf_count, 1)
        self.assertEqual(stats.graph_depth, 2)
        self.assertEqual(stats.isolated_nodes, 0)

    def test_diamond_graph(self) -> None:
        nodes = tuple(ExecutionNode(node_id=c, node_type=NodeType.STEP, payload=c) for c in "abcd")
        edges = (
            ExecutionEdge(source_id="a", target_id="b", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="a", target_id="c", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="b", target_id="d", edge_type=EdgeType.DEPENDENCY),
            ExecutionEdge(source_id="c", target_id="d", edge_type=EdgeType.DEPENDENCY),
        )
        graph = ExecutionGraph(nodes=nodes, edges=edges)
        stats = self._compute(graph)

        self.assertEqual(stats.root_count, 1)
        self.assertEqual(stats.leaf_count, 1)
        self.assertEqual(stats.graph_width, 2)  # b and c at level 1
        self.assertEqual(stats.parallel_branches, 1)

    def test_isolated_nodes(self) -> None:
        nodes = tuple(ExecutionNode(node_id=c, node_type=NodeType.STEP, payload=c) for c in "abc")
        graph = ExecutionGraph(nodes=nodes, edges=())
        stats = self._compute(graph)

        self.assertEqual(stats.isolated_nodes, 3)
        self.assertEqual(stats.root_count, 3)
        self.assertEqual(stats.leaf_count, 3)


if __name__ == "__main__":
    unittest.main()
