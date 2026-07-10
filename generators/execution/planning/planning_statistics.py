"""Planning statistics."""

from dataclasses import dataclass

@dataclass
class PlanningStatistics:
    """
    Mutable container for planning metrics.
    
    Attributes:
        stage_count: Total number of execution stages.
        phase_count: Total number of execution phases.
        batch_count: Total number of execution batches.
        parallel_groups: Number of groups that can run in parallel.
        execution_depth: The maximum depth of the execution plan.
        dependency_groups: Number of dependency-bound groups.
        critical_path_length: Length of the critical path.
    """
    stage_count: int = 0
    phase_count: int = 0
    batch_count: int = 0
    parallel_groups: int = 0
    execution_depth: int = 0
    dependency_groups: int = 0
    critical_path_length: int = 0
