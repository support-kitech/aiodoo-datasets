"""Constraint knowledge container."""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ConstraintKnowledge:
    """Extracted environmental limitation."""

    operation_ref: str | None
    constraint_type: str
    raw_description: str
