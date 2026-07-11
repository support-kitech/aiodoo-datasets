"""Export configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ExportConfig:
    """Immutable configuration for the export phase."""

    output_directory: Path
    compress_output: bool = False
    generate_manifest: bool = True
    generate_metadata: bool = True
