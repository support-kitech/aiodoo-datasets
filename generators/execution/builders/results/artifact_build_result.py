from dataclasses import dataclass
from generators.execution.builders.results.base import BaseBuildResult
from generators.execution.artifacts.artifact import Artifact


@dataclass(frozen=True, slots=True)
class ArtifactBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the ArtifactBuilder."""

    artifacts: tuple[Artifact, ...]
