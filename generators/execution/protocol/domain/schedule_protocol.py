"""Schedule protocol serialization model."""

from dataclasses import dataclass, field
from generators.execution.protocol.domain.batch_protocol import BatchProtocol


@dataclass(frozen=True, slots=True)
class ScheduleProtocol:
    """
    Immutable representation of an execution schedule for protocol serialization.

    Attributes:
        schedule_id: Identifier for the schedule.
        strategy: Strategy used to build the schedule.
        batches: Tuple of serialized batches in this schedule.
    """

    schedule_id: str
    strategy: str
    batches: tuple[BatchProtocol, ...] = field(default_factory=tuple)
