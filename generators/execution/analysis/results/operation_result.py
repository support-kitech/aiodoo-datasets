"""Operation result container."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.analysis.knowledge.operation_knowledge import (
    OperationKnowledge,
)


@dataclass(frozen=True, eq=True)
class OperationResult:
    """Result of operation analysis."""

    is_successful: bool
    operations: tuple[OperationKnowledge, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
