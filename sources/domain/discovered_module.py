"""Internal domain model for raw discovered modules."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DiscoveredModule:
    """Raw module data discovered by the scanner, before interpretation."""

    module_path: Path
    manifest_path: Path
    raw_manifest: str
    repository_path: Path
