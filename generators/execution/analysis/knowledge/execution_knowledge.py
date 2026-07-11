"""Execution knowledge container."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.analysis.knowledge.operation_knowledge import (
    OperationKnowledge,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.dependency_knowledge import (
    DependencyKnowledge,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.constraint_knowledge import (
    ConstraintKnowledge,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.verification_knowledge import (
    VerificationKnowledge,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.rollback_knowledge import (
    RollbackKnowledge,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.artifact_knowledge import (
    ArtifactKnowledge,
)


@dataclass(frozen=True, eq=True)
class ExecutionKnowledge:
    """
    Root knowledge container assembling completely distinct extraction streams.
    Passed to Builders for formal translation.
    """

    artifacts: tuple[ArtifactKnowledge, ...] = field(default_factory=tuple)
    operations: tuple[OperationKnowledge, ...] = field(default_factory=tuple)
    dependencies: tuple[DependencyKnowledge, ...] = field(default_factory=tuple)
    constraints: tuple[ConstraintKnowledge, ...] = field(default_factory=tuple)
    verifications: tuple[VerificationKnowledge, ...] = field(default_factory=tuple)
    rollbacks: tuple[RollbackKnowledge, ...] = field(default_factory=tuple)
