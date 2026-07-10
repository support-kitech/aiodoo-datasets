"""Phase protocol serialization model."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.protocol.domain.stage_protocol import StageProtocol

@dataclass(frozen=True, slots=True)
class PhaseProtocol:
    """
    Immutable representation of an execution phase for protocol serialization.
    
    Attributes:
        phase_id: Identifier for the phase.
        name: Name of the phase.
        stages: Tuple of serialized stages in this phase.
    """
    phase_id: str
    name: str
    stages: tuple[StageProtocol, ...] = field(default_factory=tuple)
