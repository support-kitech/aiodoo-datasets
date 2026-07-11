"""Pipeline statistics for the Protocol Framework."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineStatistics:
    """
    Immutable statistics collected during protocol assembly.
    Observational only.
    """

    objects_created: int = 0
    relationships_created: int = 0
    references_created: int = 0
    validation_count: int = 0
    serialization_count: int = 0
    assembly_duration_ms: float = 0.0
    validation_duration_ms: float = 0.0
    serialization_duration_ms: float = 0.0
    export_duration_ms: float = 0.0
