from dataclasses import dataclass


@dataclass
class BuilderStatistics:
    """
    Mutable state tracker for tracking metrics across the pipeline.
    """

    builder_execution_count: int = 0
    factory_execution_count: int = 0
    validation_execution_count: int = 0
    pipeline_execution_count: int = 0

    successful_builders: int = 0
    failed_builders: int = 0
    skipped_builders: int = 0

    average_build_time: float = 0.0
    diagnostics_count: int = 0
    warning_count: int = 0
    error_count: int = 0
