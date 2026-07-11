"""DFS-based cycle detection for ExecutionGraph."""

from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.exceptions import CycleDetectedError


class CycleDetector:
    """
    Performs DFS-based cycle detection on an ExecutionGraph.

    Returns immutable diagnostics listing all detected circular paths.
    Raises CycleDetectedError when cycles are found.
    """

    @staticmethod
    def detect(graph: ExecutionGraph) -> tuple[tuple[str, ...], ...]:
        """
        Detects all cycles in the graph using iterative DFS.

        Returns:
            Empty tuple if acyclic, otherwise raises CycleDetectedError.
        """
        adjacency: dict[str, list[str]] = {}
        for node in graph.nodes:
            adjacency[node.node_id] = []
        for edge in graph.edges:
            if edge.source_id in adjacency:
                adjacency[edge.source_id].append(edge.target_id)

        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {nid: WHITE for nid in adjacency}
        parent: dict[str, str | None] = {nid: None for nid in adjacency}
        cycles: list[tuple[str, ...]] = []

        for start_id in sorted(adjacency.keys()):
            if color[start_id] != WHITE:
                continue

            stack = [start_id]
            while stack:
                node_id = stack[-1]

                if color[node_id] == WHITE:
                    color[node_id] = GRAY
                    for neighbor in sorted(adjacency.get(node_id, [])):
                        if color[neighbor] == WHITE:
                            parent[neighbor] = node_id
                            stack.append(neighbor)
                        elif color[neighbor] == GRAY:
                            # Cycle found — reconstruct path
                            cycle_path = [neighbor, node_id]
                            p = node_id
                            while p != neighbor and parent.get(p) is not None:
                                p = parent[p]  # type: ignore[assignment]
                                cycle_path.append(p)
                            cycles.append(tuple(reversed(cycle_path)))
                else:
                    stack.pop()
                    color[node_id] = BLACK

        if cycles:
            raise CycleDetectedError(cycles=tuple(cycles))

        return ()
