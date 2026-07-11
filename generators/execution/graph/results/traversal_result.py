"""Traversal result."""

from dataclasses import dataclass
from generators.execution.graph.node import ExecutionNode
from generators.execution.graph.enums import TraversalStrategy


@dataclass(frozen=True, slots=True)
class TraversalResult:
    """Immutable result from GraphTraversal."""

    success: bool
    nodes: tuple[ExecutionNode, ...]
    strategy: TraversalStrategy
