"""Export statistics tracker."""

from dataclasses import dataclass

@dataclass
class ExportStatistics:
    """
    Mutable container for export metrics.
    
    Attributes:
        jsonl_records: Number of JSONL records written.
        exported_files: Total number of files generated.
        exported_bytes: Total bytes written to disk.
        manifest_count: Number of manifest files written.
        metadata_count: Number of metadata files written.
        writer_execution_count: Number of writers executed.
        validation_execution_count: Number of validators executed.
        export_duration: Time taken to complete the export.
    """
    jsonl_records: int = 0
    exported_files: int = 0
    exported_bytes: int = 0
    manifest_count: int = 0
    metadata_count: int = 0
    writer_execution_count: int = 0
    validation_execution_count: int = 0
    export_duration: float = 0.0
