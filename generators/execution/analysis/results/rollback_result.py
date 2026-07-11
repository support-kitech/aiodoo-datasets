"""Rollback result container."""

from dataclasses import dataclass, field
from generators.execution.analysis.knowledge.rollback_knowledge import (
    RollbackKnowledge,
)


@dataclass(frozen=True, eq=True)
class RollbackResult:
    """Result of rollback analysis."""

    is_successful: bool
    rollbacks: tuple[RollbackKnowledge, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
