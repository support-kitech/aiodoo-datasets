"""Python engineering artifact."""

from dataclasses import dataclass
from generators.execution.artifacts.artifact import Artifact
from generators.execution.artifacts.enums import PythonArtifactType


@dataclass(frozen=True, eq=True)
class PythonArtifact(Artifact):  # type: ignore[misc]
    """
    Represents a Python-based execution target.

    Attributes:
        artifact_type: The specific type of Python artifact.
    """

    artifact_type: PythonArtifactType
