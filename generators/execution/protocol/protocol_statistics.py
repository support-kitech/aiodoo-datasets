"""Protocol mapping and serialization statistics."""

from dataclasses import dataclass


@dataclass
class ProtocolStatistics:
    """
    Mutable container for protocol metrics.

    Attributes:
        mapped_plans: Number of plans mapped.
        mapped_stages: Number of stages mapped.
        mapped_phases: Number of phases mapped.
        mapped_batches: Number of batches mapped.
        mapped_schedules: Number of schedules mapped.
        serialization_count: Number of times serialization occurred.
        validation_count: Number of times validation occurred.
        protocol_size_bytes: Size of the serialized protocol in bytes.
    """

    mapped_plans: int = 0
    mapped_stages: int = 0
    mapped_phases: int = 0
    mapped_batches: int = 0
    mapped_schedules: int = 0
    serialization_count: int = 0
    validation_count: int = 0
    protocol_size_bytes: int = 0
