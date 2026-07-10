"""Python engineering artifact."""

from dataclasses import dataclass
from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact
from aiodoo_datasets.generators.execution.artifacts.enums import PythonArtifactType

@dataclass(frozen=True, eq=True)
class PythonArtifact(Artifact):
    """
    Represents a Python-based execution target.
    
    Attributes:
        artifact_type: The specific type of Python artifact.
    """
    artifact_type: PythonArtifactType
