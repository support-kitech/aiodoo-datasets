"""Domain model for discovered structural knowledge."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextKnowledge:
    """Strongly typed container for parsed engineering artifacts."""

    module_name: str
    python_files: dict[str, Any] = field(default_factory=dict)
    xml_files: dict[str, Any] = field(default_factory=dict)
    manifest: dict[str, Any] = field(default_factory=dict)
    security: dict[str, Any] = field(default_factory=dict)
