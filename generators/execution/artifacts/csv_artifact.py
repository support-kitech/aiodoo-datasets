"""CSV engineering artifact."""

from dataclasses import dataclass
from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact
from aiodoo_datasets.generators.execution.artifacts.enums import CSVArtifactType

@dataclass(frozen=True, eq=True)
class CSVArtifact(Artifact):
    """
    Represents a CSV-based execution target.
    
    Attributes:
        artifact_type: The specific type of CSV artifact.
    """
    artifact_type: CSVArtifactType
