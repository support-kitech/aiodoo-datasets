from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SkippedItem:
    """Tracks an item intentionally skipped due to lack of support or irrelevance."""
    source: str
    reason: str
