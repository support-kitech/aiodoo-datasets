"""Enums for the Integration package."""

from enum import Enum, unique


@unique
class PipelinePhase(Enum):
    """Phases of the integration pipeline."""

    DISCOVERY = "DISCOVERY"
    ANALYSIS = "ANALYSIS"
    BUILDERS = "BUILDERS"
    GRAPH = "GRAPH"
    PLANNING = "PLANNING"
    PROTOCOL = "PROTOCOL"
    EXPORT = "EXPORT"
