"""Rollback knowledge container."""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class RollbackKnowledge:
    """Extracted recovery strategy for operation failure."""

    operation_ref: str
    reversion_command: str
    explanation: str
