"""Observational statistics for the validation pipeline."""

from dataclasses import dataclass, field
from typing import Mapping
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class PipelineStatistics:
    """Timing and counter data for the validation pipeline execution."""

    datasets_validated: int = 0
    records_validated: int = 0
    rules_executed: int = 0
    total_duration_ms: float = 0.0
    per_dataset_durations: Mapping[str, float] = field(default_factory=lambda: MappingProxyType({}))
