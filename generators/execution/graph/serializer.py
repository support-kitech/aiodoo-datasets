"""Deterministic graph serialization."""

import json
from generators.execution.graph.graph import ExecutionGraph


class GraphSerializer:
    """
    Deterministic serialization of graph state.

    No Protocol mapping. Only graph snapshot.
    Produces identical output for identical graphs.
    """

    @staticmethod
    def serialize(graph: ExecutionGraph) -> str:
        """Serializes the graph to a deterministic JSON string."""
        nodes = sorted(
            [
                {
                    "node_id": n.node_id,
                    "node_type": n.node_type.name,
                    "depth": n.depth,
                }
                for n in graph.nodes
            ],
            key=lambda x: x["node_id"],
        )

        edges = sorted(
            [
                {
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "edge_type": e.edge_type.name,
                    "weight": e.weight,
                }
                for e in graph.edges
            ],
            key=lambda x: (x["source_id"], x["target_id"]),
        )

        return json.dumps(
            {"nodes": nodes, "edges": edges},
            sort_keys=True,
            separators=(",", ":"),
        )
