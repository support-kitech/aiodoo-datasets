"""Immutable graph edge connecting two nodes."""

from dataclasses import dataclass
from typing import Any
from aiodoo_datasets.generators.execution.graph.enums import EdgeType
from aiodoo_datasets.generators.execution.graph.node import NodeId


@dataclass(frozen=True)
class ExecutionEdge:
    """
    An immutable directed edge in the ExecutionGraph.

    Identity is determined by the (source_id, target_id) pair.
    """
    source_id: NodeId
    target_id: NodeId
    edge_type: EdgeType
    weight: float = 1.0

    def __hash__(self) -> int:
        return hash((self.source_id, self.target_id))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExecutionEdge):
            return NotImplemented
        return (self.source_id, self.target_id) == (other.source_id, other.target_id)
