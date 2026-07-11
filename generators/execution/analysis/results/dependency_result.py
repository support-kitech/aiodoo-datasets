"""Dependency result container."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.analysis.knowledge.dependency_knowledge import (
    DependencyKnowledge,
)


@dataclass(frozen=True, eq=True)
class DependencyResult:
    """Result of dependency analysis."""

    is_successful: bool
    dependencies: tuple[DependencyKnowledge, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
