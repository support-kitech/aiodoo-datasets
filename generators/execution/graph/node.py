"""Immutable graph node wrapping a domain object."""

from dataclasses import dataclass, field
from typing import Any
from types import MappingProxyType
from generators.execution.graph.enums import NodeType


NodeId = str


@dataclass(frozen=True)
class ExecutionNode:
    """
    An immutable vertex in the ExecutionGraph.

    Wraps a Phase 1 domain object with graph-specific metadata.
    Identity is determined exclusively by node_id.
    """

    node_id: NodeId
    node_type: NodeType
    payload: Any
    depth: int = 0
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))  # type: ignore[type-arg]

    def __hash__(self) -> int:
        return hash(self.node_id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExecutionNode):
            return NotImplemented
        return self.node_id == other.node_id

    def __lt__(self, other: "ExecutionNode") -> bool:
        if not isinstance(other, ExecutionNode):
            return NotImplemented
        return self.node_id < other.node_id
