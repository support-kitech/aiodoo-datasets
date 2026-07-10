"""Engineering artifacts representing physical or logical execution targets."""

from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact
from aiodoo_datasets.generators.execution.artifacts.python_artifact import PythonArtifact
from aiodoo_datasets.generators.execution.artifacts.xml_artifact import XMLArtifact
from aiodoo_datasets.generators.execution.artifacts.csv_artifact import CSVArtifact
from aiodoo_datasets.generators.execution.artifacts.enums import PythonArtifactType, XMLArtifactType, CSVArtifactType

__all__ = [
    "Artifact",
    "PythonArtifact",
    "XMLArtifact",
    "CSVArtifact",
    "PythonArtifactType",
    "XMLArtifactType",
    "CSVArtifactType",
]
