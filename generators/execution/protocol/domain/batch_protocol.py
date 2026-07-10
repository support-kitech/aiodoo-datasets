"""Batch protocol serialization model."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.protocol.domain.phase_protocol import PhaseProtocol

@dataclass(frozen=True, slots=True)
class BatchProtocol:
    """
    Immutable representation of an execution batch for protocol serialization.
    
    Attributes:
        batch_id: Identifier for the batch.
        is_parallel: Whether phases can run in parallel.
        phases: Tuple of serialized phases in this batch.
    """
    batch_id: str
    is_parallel: bool
    phases: tuple[PhaseProtocol, ...] = field(default_factory=tuple)
