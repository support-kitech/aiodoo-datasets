"""Pipeline statistics tracker."""

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class PipelineStatistics:
    """
    Mutable container for pipeline metrics.
    
    Attributes:
        total_execution_time: Total duration of pipeline execution.
        phase_execution_times: Duration of each phase.
        generated_records: Number of records generated.
        exported_files: Number of files exported.
        validation_failures: Number of validation failures encountered.
        warnings: Number of warnings encountered.
        errors: Number of errors encountered.
    """
    total_execution_time: float = 0.0
    phase_execution_times: Dict[str, float] = field(default_factory=dict)
    generated_records: int = 0
    exported_files: int = 0
    validation_failures: int = 0
    warnings: int = 0
    errors: int = 0
