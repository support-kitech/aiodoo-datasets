"""Configuration options for pipeline execution."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineOptions:
    """Immutable options dictating how the pipeline operates."""

    force_rescan: bool = False
    skip_cache: bool = False
    validate_only: bool = False
    scan_only: bool = False
