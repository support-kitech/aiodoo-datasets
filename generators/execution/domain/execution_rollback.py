"""Immutable representation of execution failure recovery."""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ExecutionRollback:
    """
    Defines recovery logic to undo the operation if failure occurs.

    Attributes:
        command: The shell command or script to execute to revert changes.
        description: Human-readable explanation of the rollback strategy.
    """

    command: str
    description: str
