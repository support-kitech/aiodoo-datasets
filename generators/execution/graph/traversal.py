"""Non-mutating graph traversal supporting multiple strategies."""

from collections import deque
from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.node import ExecutionNode, NodeId
from generators.execution.graph.enums import TraversalStrategy, EdgeType
from generators.execution.graph.results.traversal_result import TraversalResult


class GraphTraversal:
    """
    Performs read-only traversal of an ExecutionGraph.

    Supports DFS, BFS, reverse, dependency, and rollback strategies.
    Never mutates the graph.
    """

    @staticmethod
    def traverse(
        graph: ExecutionGraph,
        strategy: TraversalStrategy,
        start_node_id: NodeId | None = None,
    ) -> TraversalResult:
        """Traverses the graph using the given strategy."""
        if strategy == TraversalStrategy.DFS:
            nodes = GraphTraversal._dfs(graph, start_node_id)
        elif strategy == TraversalStrategy.BFS:
            nodes = GraphTraversal._bfs(graph, start_node_id)
        elif strategy == TraversalStrategy.REVERSE:
            nodes = GraphTraversal._reverse(graph, start_node_id)
        elif strategy == TraversalStrategy.DEPENDENCY:
            nodes = GraphTraversal._dependency(graph, start_node_id)
        elif strategy == TraversalStrategy.ROLLBACK:
            nodes = GraphTraversal._rollback(graph, start_node_id)
        else:
            nodes = ()

        return TraversalResult(
            success=True,
            nodes=nodes,
            strategy=strategy,
        )

    @staticmethod
    def _dfs(graph: ExecutionGraph, start_id: NodeId | None) -> tuple[ExecutionNode, ...]:
        """Depth-first traversal from roots or a specific start node."""
        adjacency = GraphTraversal._build_adjacency(graph)
        starts = [start_id] if start_id else [n.node_id for n in graph.roots]
        visited: set[str] = set()
        result: list[ExecutionNode] = []
        node_map = {n.node_id: n for n in graph.nodes}

        for s in sorted(starts):
            stack = [s]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                if current in node_map:
                    result.append(node_map[current])
                for neighbor in sorted(adjacency.get(current, []), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return tuple(result)

    @staticmethod
    def _bfs(graph: ExecutionGraph, start_id: NodeId | None) -> tuple[ExecutionNode, ...]:
        """Breadth-first traversal from roots or a specific start node."""
        adjacency = GraphTraversal._build_adjacency(graph)
        starts = [start_id] if start_id else [n.node_id for n in graph.roots]
        visited: set[str] = set()
        result: list[ExecutionNode] = []
        node_map = {n.node_id: n for n in graph.nodes}
        queue: deque[str] = deque(sorted(starts))

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if current in node_map:
                result.append(node_map[current])
            for neighbor in sorted(adjacency.get(current, [])):
                if neighbor not in visited:
                    queue.append(neighbor)
        return tuple(result)

    @staticmethod
    def _reverse(graph: ExecutionGraph, start_id: NodeId | None) -> tuple[ExecutionNode, ...]:
        """Reverse traversal from leaves or a specific start node, following incoming edges."""
        reverse_adj = GraphTraversal._build_reverse_adjacency(graph)
        starts = [start_id] if start_id else [n.node_id for n in graph.leaves]
        visited: set[str] = set()
        result: list[ExecutionNode] = []
        node_map = {n.node_id: n for n in graph.nodes}

        for s in sorted(starts):
            stack = [s]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                if current in node_map:
                    result.append(node_map[current])
                for neighbor in sorted(reverse_adj.get(current, []), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return tuple(result)

    @staticmethod
    def _dependency(graph: ExecutionGraph, start_id: NodeId | None) -> tuple[ExecutionNode, ...]:
        """Traverses only DEPENDENCY edges via DFS."""
        dep_adj: dict[str, list[str]] = {n.node_id: [] for n in graph.nodes}
        for edge in graph.edges:
            if edge.edge_type == EdgeType.DEPENDENCY and edge.source_id in dep_adj:
                dep_adj[edge.source_id].append(edge.target_id)

        starts = [start_id] if start_id else [n.node_id for n in graph.roots]
        visited: set[str] = set()
        result: list[ExecutionNode] = []
        node_map = {n.node_id: n for n in graph.nodes}

        for s in sorted(starts):
            stack = [s]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                if current in node_map:
                    result.append(node_map[current])
                for neighbor in sorted(dep_adj.get(current, []), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return tuple(result)

    @staticmethod
    def _rollback(graph: ExecutionGraph, start_id: NodeId | None) -> tuple[ExecutionNode, ...]:
        """Traverses only ROLLBACK edges via DFS."""
        rb_adj: dict[str, list[str]] = {n.node_id: [] for n in graph.nodes}
        for edge in graph.edges:
            if edge.edge_type == EdgeType.ROLLBACK and edge.source_id in rb_adj:
                rb_adj[edge.source_id].append(edge.target_id)

        starts = [start_id] if start_id else sorted([n.node_id for n in graph.nodes])
        visited: set[str] = set()
        result: list[ExecutionNode] = []
        node_map = {n.node_id: n for n in graph.nodes}

        for s in sorted(starts):
            stack = [s]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                if current in node_map:
                    result.append(node_map[current])
                for neighbor in sorted(rb_adj.get(current, []), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return tuple(result)

    @staticmethod
    def _build_adjacency(graph: ExecutionGraph) -> dict[str, list[str]]:
        adj: dict[str, list[str]] = {n.node_id: [] for n in graph.nodes}
        for edge in graph.edges:
            if edge.source_id in adj:
                adj[edge.source_id].append(edge.target_id)
        return adj

    @staticmethod
    def _build_reverse_adjacency(graph: ExecutionGraph) -> dict[str, list[str]]:
        adj: dict[str, list[str]] = {n.node_id: [] for n in graph.nodes}
        for edge in graph.edges:
            if edge.target_id in adj:
                adj[edge.target_id].append(edge.source_id)
        return adj
