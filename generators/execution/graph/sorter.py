"""Deterministic topological sort with secondary alphanumeric ordering."""

from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.detector import CycleDetector
from aiodoo_datasets.generators.execution.graph.results.sort_result import SortResult


class TopologicalSorter:
    """
    Performs a deterministic topological sort on an ExecutionGraph.

    Uses Kahn's algorithm with a secondary alphanumeric sort on node_id
    to guarantee stable, reproducible output. Delegates cycle safety
    to CycleDetector.
    """

    @staticmethod
    def sort(graph: ExecutionGraph) -> SortResult:
        """
        Returns a SortResult containing the topologically sorted nodes.
        Raises CycleDetectedError if cycles exist.
        """
        # Fail fast on cycles
        CycleDetector.detect(graph)

        # Build adjacency and in-degree maps
        in_degree: dict[str, int] = {n.node_id: 0 for n in graph.nodes}
        adjacency: dict[str, list[str]] = {n.node_id: [] for n in graph.nodes}
        node_map: dict[str, ExecutionNode] = {n.node_id: n for n in graph.nodes}

        for edge in graph.edges:
            if edge.target_id in in_degree:
                in_degree[edge.target_id] += 1
            if edge.source_id in adjacency:
                adjacency[edge.source_id].append(edge.target_id)

        # Kahn's algorithm with alphanumeric secondary ordering
        queue = sorted([nid for nid, deg in in_degree.items() if deg == 0])
        sorted_nodes: list[ExecutionNode] = []

        while queue:
            current = queue.pop(0)
            sorted_nodes.append(node_map[current])

            for neighbor in sorted(adjacency.get(current, [])):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    # Insert in sorted position for determinism
                    inserted = False
                    for i, q_item in enumerate(queue):
                        if neighbor < q_item:
                            queue.insert(i, neighbor)
                            inserted = True
                            break
                    if not inserted:
                        queue.append(neighbor)

        return SortResult(
            success=True,
            sorted_nodes=tuple(sorted_nodes),
            has_cycles=False,
        )
