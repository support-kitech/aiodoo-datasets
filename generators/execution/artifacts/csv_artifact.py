"""CSV engineering artifact."""

from dataclasses import dataclass
from generators.execution.artifacts.artifact import Artifact
from generators.execution.artifacts.enums import CSVArtifactType


@dataclass(frozen=True, eq=True)
class CSVArtifact(Artifact):  # type: ignore[misc]
    """
    Represents a CSV-based execution target.

    Attributes:
        artifact_type: The specific type of CSV artifact.
    """

    artifact_type: CSVArtifactType
