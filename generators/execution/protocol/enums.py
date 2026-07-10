"""Enums for the Protocol package."""

from enum import Enum, unique

@unique
class ProtocolType(Enum):
    """Types of protocol objects."""
    EXECUTION = "EXECUTION"
    STAGE = "STAGE"
    PHASE = "PHASE"
    BATCH = "BATCH"
    SCHEDULE = "SCHEDULE"
    METADATA = "METADATA"
