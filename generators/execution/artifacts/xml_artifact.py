"""XML engineering artifact."""

from dataclasses import dataclass
from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact
from aiodoo_datasets.generators.execution.artifacts.enums import XMLArtifactType


@dataclass(frozen=True, eq=True)
class XMLArtifact(Artifact):
    """
    Represents an XML-based execution target.

    Attributes:
        artifact_type: The specific type of XML artifact.
    """

    artifact_type: XMLArtifactType
