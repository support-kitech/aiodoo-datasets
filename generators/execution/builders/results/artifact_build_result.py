from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact


@dataclass(frozen=True, slots=True)
class ArtifactBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the ArtifactBuilder."""

    artifacts: tuple[Artifact, ...]
