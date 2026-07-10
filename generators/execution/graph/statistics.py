"""Mutable graph statistics tracker."""

from dataclasses import dataclass


@dataclass
class GraphStatistics:
    """
    Tracks structural metrics of the ExecutionGraph.
    Mutable during computation, frozen after pipeline completes.
    """
    node_count: int = 0
    edge_count: int = 0
    root_count: int = 0
    leaf_count: int = 0
    graph_depth: int = 0
    graph_width: int = 0
    longest_path: int = 0
    parallel_branches: int = 0
    isolated_nodes: int = 0
