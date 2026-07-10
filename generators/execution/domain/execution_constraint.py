"""Immutable representation of an execution constraint."""

from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class ExecutionConstraint:
    """
    Defines environmental or situational conditions required for execution.
    
    Attributes:
        description: Natural language explanation of the constraint.
        is_hard_constraint: If True, failure to meet this aborts execution.
    """
    description: str
    is_hard_constraint: bool = True
