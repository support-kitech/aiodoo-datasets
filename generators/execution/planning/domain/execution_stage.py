"""Immutable representation of an execution stage."""

from dataclasses import dataclass, field
from generators.execution.graph.node import ExecutionNode
from generators.execution.planning.enums import StageType


@dataclass(frozen=True, slots=True)
class ExecutionStage:
    """
    A specific stage of execution containing a set of nodes.

    Attributes:
        stage_id: Unique identifier for the stage.
        stage_type: The type of stage.
        nodes: Topologically ordered tuple of execution nodes in this stage.
    """

    stage_id: str
    stage_type: StageType
    nodes: tuple[ExecutionNode, ...] = field(default_factory=tuple)

    def __hash__(self) -> int:
        return hash(self.stage_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExecutionStage):
            return NotImplemented
        return self.stage_id == other.stage_id
