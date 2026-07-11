"""Immutable execution graph."""

from dataclasses import dataclass, field
from typing import Optional
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode, NodeId
from aiodoo_datasets.generators.execution.graph.edge import ExecutionEdge


@dataclass(frozen=True)
class ExecutionGraph:
    """
    An immutable directed acyclic graph of ExecutionNodes and ExecutionEdges.

    Stores only domain objects. Never Knowledge, never Protocol.
    Provides read-only lookup helpers.
    """

    nodes: tuple[ExecutionNode, ...] = field(default_factory=tuple)
    edges: tuple[ExecutionEdge, ...] = field(default_factory=tuple)

    def get_node(self, node_id: NodeId) -> Optional[ExecutionNode]:
        """Returns the node matching node_id, or None."""
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_edges_from(self, node_id: NodeId) -> tuple[ExecutionEdge, ...]:
        """Returns all outgoing edges from a given node."""
        return tuple(e for e in self.edges if e.source_id == node_id)

    def get_edges_to(self, node_id: NodeId) -> tuple[ExecutionEdge, ...]:
        """Returns all incoming edges to a given node."""
        return tuple(e for e in self.edges if e.target_id == node_id)

    @property
    def roots(self) -> tuple[ExecutionNode, ...]:
        """Returns nodes with no incoming edges (entry points)."""
        targets = {e.target_id for e in self.edges}
        return tuple(sorted(n for n in self.nodes if n.node_id not in targets))

    @property
    def leaves(self) -> tuple[ExecutionNode, ...]:
        """Returns nodes with no outgoing edges (terminal points)."""
        sources = {e.source_id for e in self.edges}
        return tuple(sorted(n for n in self.nodes if n.node_id not in sources))
