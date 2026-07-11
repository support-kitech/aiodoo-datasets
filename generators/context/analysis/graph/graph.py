"""Domain model for the Context Graph orchestrating nodes and edges."""

from typing import Any
from generators.context.analysis.graph.node import ContextNode
from generators.context.analysis.graph.edge import ContextEdge
from generators.context.analysis.graph.enums import NodeType, RelationshipType


class ContextGraph:
    """A deterministic, directed engineering graph representing Odoo modules."""

    def __init__(self) -> None:
        self._nodes: dict[str, ContextNode] = {}
        self._edges: dict[str, ContextEdge] = {}

    def add_node(self, node: ContextNode) -> None:
        """Add a node to the graph. Raises ValueError if it already exists."""
        if node.node_id in self._nodes:
            raise ValueError(f"Node with ID {node.node_id} already exists.")
        self._nodes[node.node_id] = node

    def add_edge(self, edge: ContextEdge) -> None:
        """Add an edge to the graph. Raises ValueError if edge already exists or nodes are missing."""
        if edge.edge_id in self._edges:
            raise ValueError(f"Edge with ID {edge.edge_id} already exists.")
        if edge.source_id not in self._nodes:
            raise ValueError(f"Source node {edge.source_id} does not exist.")
        if edge.target_id not in self._nodes:
            raise ValueError(f"Target node {edge.target_id} does not exist.")
        self._edges[edge.edge_id] = edge

    def get_node(self, node_id: str) -> ContextNode:
        """Retrieve a node by its ID. Raises KeyError if not found."""
        return self._nodes[node_id]

    def get_outgoing_edges(self, node_id: str) -> list[ContextEdge]:
        """Retrieve all outbound edges from the specified node_id. Deterministically sorted."""
        if node_id not in self._nodes:
            raise KeyError(f"Node {node_id} does not exist.")
        edges = [e for e in self._edges.values() if e.source_id == node_id]
        return sorted(edges)

    def get_incoming_edges(self, node_id: str) -> list[ContextEdge]:
        """Retrieve all inbound edges to the specified node_id. Deterministically sorted."""
        if node_id not in self._nodes:
            raise KeyError(f"Node {node_id} does not exist.")
        edges = [e for e in self._edges.values() if e.target_id == node_id]
        return sorted(edges)

    def get_neighbors(self, node_id: str) -> list[ContextEdge]:
        """Retrieve both inbound and outbound edges for the specified node_id. Deterministically sorted."""
        outgoing = self.get_outgoing_edges(node_id)
        incoming = self.get_incoming_edges(node_id)
        # Using a set to prevent duplicates if a node connects to itself
        combined = set(outgoing) | set(incoming)
        return sorted(combined)

    def get_edges(self) -> list[ContextEdge]:
        """Retrieve all edges in the graph. Deterministically sorted."""
        return sorted(self._edges.values())

    def get_nodes(self) -> list[ContextNode]:
        """Retrieve all nodes in the graph. Deterministically sorted."""
        return sorted(self._nodes.values())

    def find_nodes_by_type(self, node_type: NodeType) -> list[ContextNode]:
        """Find all nodes of a specific type. Deterministically sorted."""
        nodes = [n for n in self._nodes.values() if n.node_type == node_type]
        return sorted(nodes)

    def find_edges_by_type(self, relationship_type: RelationshipType) -> list[ContextEdge]:
        """Find all edges of a specific relationship type. Deterministically sorted."""
        edges = [e for e in self._edges.values() if e.relationship_type == relationship_type]
        return sorted(edges)

    def contains_node(self, node_id: str) -> bool:
        """Check if a node exists in the graph."""
        return node_id in self._nodes

    def contains_edge(self, edge_id: str) -> bool:
        """Check if an edge exists in the graph."""
        return edge_id in self._edges

    def node_count(self) -> int:
        """Return the total number of nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Return the total number of edges."""
        return len(self._edges)

    def to_dict(self) -> dict[str, Any]:
        """Deterministically serialize the entire graph to a dictionary."""
        return {
            "nodes": [node.to_dict() for node in self.get_nodes()],
            "edges": [edge.to_dict() for edge in self.get_edges()],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextGraph":
        """Deserialize a ContextGraph from a dictionary."""
        graph = cls()
        for node_data in data.get("nodes", []):
            graph.add_node(ContextNode.from_dict(node_data))
        for edge_data in data.get("edges", []):
            graph.add_edge(ContextEdge.from_dict(edge_data))
        return graph
