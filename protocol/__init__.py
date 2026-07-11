"""
AIODOO Protocol Framework

The canonical contract layer for the AIODOO ecosystem.
Defines immutable, deterministic, versioned protocol objects
that serve as the shared language across all frameworks and generators.
"""

from protocol.constants.framework import PROTOCOL_FRAMEWORK_VERSION
from protocol.exceptions import ProtocolError

from protocol.domain.identifiers import ProtocolIdentifier
from protocol.domain.enums import ProtocolType, ReferenceType, RelationshipType, ExportFormat
from protocol.domain.version import ProtocolVersion
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship
from protocol.domain.metadata import ProtocolMetadata
from protocol.domain.schema import ProtocolSchema
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.dataset import ProtocolDataset, ProtocolContext

from protocol.pipeline.assembly_options import AssemblyOptions
from protocol.pipeline.pipeline_result import PipelineResult
from protocol.pipeline.pipeline_statistics import PipelineStatistics
from protocol.core.manager import ProtocolManager

__version__ = PROTOCOL_FRAMEWORK_VERSION

__all__ = [
    "PROTOCOL_FRAMEWORK_VERSION",
    "__version__",
    "ProtocolError",
    "ProtocolIdentifier",
    "ProtocolType",
    "ReferenceType",
    "RelationshipType",
    "ExportFormat",
    "ProtocolVersion",
    "ProtocolReference",
    "ProtocolRelationship",
    "ProtocolMetadata",
    "ProtocolSchema",
    "ProtocolManifest",
    "ProtocolDataset",
    "ProtocolContext",
    "AssemblyOptions",
    "PipelineResult",
    "PipelineStatistics",
    "ProtocolManager",
]
