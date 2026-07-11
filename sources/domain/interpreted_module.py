"""Internal domain model for interpreted modules."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpretedModule:
    """Module data parsed and interpreted from the manifest, before normalization."""

    technical_name: str
    module_path: Path
    manifest_path: Path
    version: str
    depends: tuple[str, ...]
    license: str | None
    installable: bool
    application: bool
    auto_install: bool
    raw_metadata: Mapping[str, Any]
