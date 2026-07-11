"""Immutable result for the Export pipeline."""

from dataclasses import dataclass
from pathlib import Path
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics


@dataclass(frozen=True, slots=True)
class ExportResult:
    """
    Result of the export process.

    Attributes:
        success: Whether the export completed successfully.
        exported_files: List of file paths generated.
        record_count: Number of records written.
        byte_count: Total bytes written.
        manifest_path: Path to the manifest file, if any.
        metadata_path: Path to the metadata file, if any.
        statistics: The final state of ExportStatistics.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    exported_files: tuple[Path, ...] = tuple()
    record_count: int = 0
    byte_count: int = 0
    manifest_path: Path | None = None
    metadata_path: Path | None = None
    statistics: ExportStatistics | None = None
    diagnostics: tuple[str, ...] = tuple()
