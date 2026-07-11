from aiodoo_datasets.generators.execution.builders.results.artifact_build_result import (
    ArtifactBuildResult,
)


class ArtifactValidator:
    """Validates Artifact domain objects."""

    @classmethod
    def validate(cls, result: ArtifactBuildResult) -> None:
        pass
