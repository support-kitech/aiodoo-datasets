"""Execution protocol serialization model."""

from dataclasses import dataclass, field
from generators.execution.protocol.domain.schedule_protocol import ScheduleProtocol
from generators.execution.protocol.domain.metadata_protocol import MetadataProtocol


@dataclass(frozen=True, slots=True)
class ExecutionProtocol:
    """
    Immutable representation of the full execution plan for protocol serialization.

    Attributes:
        plan_id: Identifier for the plan.
        graph_id: Identifier of the source graph.
        metadata: Protocol metadata including versions.
        schedules: Tuple of serialized schedules.
    """

    plan_id: str
    graph_id: str
    metadata: MetadataProtocol
    schedules: tuple[ScheduleProtocol, ...] = field(default_factory=tuple)
