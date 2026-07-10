"""Artifact result container."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.analysis.knowledge.artifact_knowledge import ArtifactKnowledge

@dataclass(frozen=True, eq=True)
class ArtifactResult:
    """Result of artifact analysis."""
    is_successful: bool
    artifacts: tuple[ArtifactKnowledge, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
