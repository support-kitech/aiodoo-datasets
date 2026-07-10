"""Common utilities for integration tests."""

import json
from pathlib import Path
from typing import List, Dict, Any

def verify_output_files(output_dir: Path, prefix: str) -> None:
    """Verify that JSONL, manifest, and statistics files exist."""
    assert (output_dir / f"{prefix}_v1_0.jsonl").exists(), f"{prefix.capitalize()} JSONL missing!"
    assert (output_dir / f"{prefix}_manifest.json").exists(), f"{prefix.capitalize()} Manifest missing!"
    assert (output_dir / f"{prefix}_statistics.json").exists(), f"{prefix.capitalize()} Statistics missing!"

def verify_jsonl_records(output_dir: Path, prefix: str) -> List[Dict[str, Any]]:
    """Read and verify JSONL records."""
    records = []
    with open(output_dir / f"{prefix}_v1_0.jsonl", "r") as f:
        for line in f:
            records.append(json.loads(line))
    assert len(records) > 0, "No records generated"
    return records
