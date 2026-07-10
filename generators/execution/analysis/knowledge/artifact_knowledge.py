"""Artifact knowledge container."""

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, eq=True)
class ArtifactKnowledge:
    """Extracted physical or logical file structure."""
    artifact_ref_id: str
    file_path: str
    symbol_name: str
    category: str
    raw_attributes: dict[str, Any] | None = None
