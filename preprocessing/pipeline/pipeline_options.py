"""Execution options for the Preprocessing Framework."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineOptions:
    """Options for executing the PreprocessingPipeline."""
    
    force_reprocess: bool = False
    skip_cache: bool = False
    validate_only: bool = False
