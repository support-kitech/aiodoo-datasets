"""Safely exports generated datasets to JSONL."""

import json
import logging
from pathlib import Path
from typing import Generic, TypeVar

import hashlib
from pydantic import BaseModel
from aiodoo_datasets.generators.common.statistics.base_statistics import BaseStatistics
from aiodoo_datasets.generators.common.export.manifest import generate_manifest

logger = logging.getLogger(__name__)

TRecord = TypeVar('TRecord', bound=BaseModel)

class DatasetWriter(Generic[TRecord]):
    """Thread-safe append-only writer for JSONL datasets with streaming statistics."""

    def __init__(self, output_dir: Path, stats: BaseStatistics, filename: str, dataset_name: str):
        self.output_dir = output_dir
        self.filename = filename
        self.dataset_name = dataset_name
        self.output_path = output_dir / filename
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.written_count = 0
        self.stats = stats

    def record_duplicate(self) -> None:
        self.stats.record_duplicate()
        
    def record_validation_failure(self) -> None:
        self.stats.record_validation_failure()

    def write_record(self, record: TRecord) -> None:
        """Serialize and append a single validated record to the JSONL file."""
        try:
            record_dict = record.model_dump()
            json_str = json.dumps(record_dict, ensure_ascii=False)
            
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(json_str + "\n")
            
            self.written_count += 1
            self.stats.add_sample(record, json_str)
        except Exception as exc:
            logger.error("Failed to write record to %s: %s", self.output_path, exc)
            
    def _calculate_checksum(self) -> str:
        """Stream the JSONL file to calculate its SHA256 checksum efficiently."""
        hasher = hashlib.sha256()
        if self.output_path.exists():
            with open(self.output_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
        return hasher.hexdigest()
            
    def export_statistics(self, filename: str = "statistics.json") -> None:
        """Dump the generated statistics to a JSON file."""
        stats_path = self.output_dir / filename
        self.stats.export(stats_path)
        logger.info("Exported statistics to %s", stats_path)
        
    def export_manifest(self, filename: str = "dataset_manifest.json") -> None:
        """Calculate the final checksum and export the dataset manifest index."""
        manifest_path = self.output_dir / filename
        checksum = self._calculate_checksum()
        
        generate_manifest(
            output_path=manifest_path,
            dataset_name=self.dataset_name,
            jsonl_filename=self.filename,
            checksum=checksum,
            stats=self.stats
        )
        logger.info("Exported dataset manifest to %s", manifest_path)
