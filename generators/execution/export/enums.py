"""Enums for the Export package."""

from enum import Enum, unique

@unique
class WriterType(Enum):
    """Types of export writers."""
    JSONL = "JSONL"
    MANIFEST = "MANIFEST"
    METADATA = "METADATA"
