"""Immutable representation of an execution prerequisite."""

from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class ExecutionDependency:
    """
    Defines a prerequisite that must complete before a step can begin.
    
    Attributes:
        depends_on_step_id: The exact deterministic ID of the required previous step.
        is_blocking: Whether a failure in the dependent step aborts this step.
    """
    depends_on_step_id: str
    is_blocking: bool = True
