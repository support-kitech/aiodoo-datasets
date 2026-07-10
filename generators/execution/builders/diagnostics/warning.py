from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Warning:
    """Represents a non-fatal execution issue (e.g. an obscure setting ignored)."""
    source: str
    message: str
    details: str = ""
