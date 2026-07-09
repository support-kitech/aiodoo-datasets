"""Dataset Manifest Generator."""

import json
from pathlib import Path
from datetime import datetime
from aiodoo_datasets.generators.common.statistics.base_statistics import BaseStatistics

def generate_manifest(
    output_path: Path,
    dataset_name: str,
    jsonl_filename: str,
    checksum: str,
    stats: BaseStatistics,
    generator_version: str = "0.1.0",
    protocol_version: str = "1.0"
) -> None:
    """Generates a complete index manifest for the generated dataset."""
    manifest = {
        "dataset_name": dataset_name,
        "generator_version": generator_version,
        "protocol_version": protocol_version,
        "generation_date": datetime.utcnow().isoformat(),
        "jsonl_filename": jsonl_filename,
        "checksum_sha256": checksum,
        
        "row_count": stats.total_samples,
        "repository_counts": stats.total_modules,
        "version_counts": dict(stats.version_distribution),
        "scenario_counts": dict(stats.scenario_distribution),
        "difficulty_distribution": dict(stats.difficulty_distribution),
    }
    
    # Merge generator-specific manifest metrics
    manifest.update(stats.get_manifest_data())
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
