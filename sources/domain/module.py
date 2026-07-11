"""Domain model for a discovered Odoo module."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class OdooModule:
    """Immutable representation of an Odoo module."""

    name: str
    technical_name: str
    path: Path
    manifest_path: Path
    version: str
    depends: tuple[str, ...]
    license: str
    installable: bool
    application: bool
    auto_install: bool
