"""Constraint result container."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.analysis.knowledge.constraint_knowledge import ConstraintKnowledge

@dataclass(frozen=True, eq=True)
class ConstraintResult:
    """Result of constraint analysis."""
    is_successful: bool
    constraints: tuple[ConstraintKnowledge, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
