from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Error:
    """Represents a fatal issue within a specific build node."""

    source: str
    message: str
    trace: str = ""
