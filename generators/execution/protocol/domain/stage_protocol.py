"""Stage protocol serialization model."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class StageProtocol:
    """
    Immutable representation of an execution stage for protocol serialization.

    Attributes:
        stage_id: Identifier for the stage.
        stage_type: Type of the stage as string.
        nodes: Tuple of node IDs or minimal representations contained in this stage.
    """

    stage_id: str
    stage_type: str
    nodes: tuple[str, ...] = field(default_factory=tuple)
