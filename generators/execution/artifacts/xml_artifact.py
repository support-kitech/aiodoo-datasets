"""XML engineering artifact."""

from dataclasses import dataclass
from generators.execution.artifacts.artifact import Artifact
from generators.execution.artifacts.enums import XMLArtifactType


@dataclass(frozen=True, eq=True)
class XMLArtifact(Artifact):  # type: ignore[misc]
    """
    Represents an XML-based execution target.

    Attributes:
        artifact_type: The specific type of XML artifact.
    """

    artifact_type: XMLArtifactType
