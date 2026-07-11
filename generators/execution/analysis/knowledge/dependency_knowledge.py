"""Dependency knowledge container."""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class DependencyKnowledge:
    """Extracted prerequisite relationship between operations."""

    source_operation_ref: str
    target_operation_ref: str
    is_hard_blocker: bool = True
