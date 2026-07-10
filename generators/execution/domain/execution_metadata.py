"""Immutable execution metadata."""

from dataclasses import dataclass, field

@dataclass(frozen=True, eq=True)
class ExecutionMetadata:
    """
    Immutable container for non-deterministic or contextual metadata.
    This data is purposefully excluded from hashing and identity checks.
    
    Attributes:
        generator_version: The version of the generator that created this.
        created_from: Reference to the source that generated this (e.g. Planner ID).
        source_locations: Map of files to lines.
        confidence: Generator confidence score [0.0, 1.0].
    """
    generator_version: str = "1.0.0"
    created_from: str | None = None
    source_locations: tuple[str, ...] = field(default_factory=tuple)
    confidence: float = 1.0
