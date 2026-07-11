"""Sort result."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode


@dataclass(frozen=True, slots=True)
class SortResult:
    """Immutable result from TopologicalSorter."""

    success: bool
    sorted_nodes: tuple[ExecutionNode, ...]
    has_cycles: bool
    cycle_paths: tuple[tuple[str, ...], ...] = field(default_factory=tuple)
