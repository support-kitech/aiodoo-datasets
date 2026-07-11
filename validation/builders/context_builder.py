"""Builds ValidationContext from the dataset directory."""

from pathlib import Path

from validation.domain.models import ValidationContext


class ContextBuilder:
    """Scans the dataset directory and builds a ValidationContext."""

    @staticmethod
    def build(dataset_dir: Path, protocol_context: object | None = None) -> ValidationContext:
        """
        Discover all JSONL, manifest, and statistics files.

        Args:
            dataset_dir: Path to the datasets/ directory.
            protocol_context: Optional ProtocolContext reference.

        Returns:
            An immutable ValidationContext.
        """
        dataset_dir = Path(dataset_dir)

        dataset_files = tuple(sorted(dataset_dir.glob("*.jsonl")))
        manifest_files = tuple(sorted(dataset_dir.glob("*manifest*.json")))
        statistics_files = tuple(sorted(dataset_dir.glob("*statistics*.json")))

        return ValidationContext(
            dataset_dir=dataset_dir,
            dataset_files=dataset_files,
            manifest_files=manifest_files,
            statistics_files=statistics_files,
            protocol_context=protocol_context,
        )
