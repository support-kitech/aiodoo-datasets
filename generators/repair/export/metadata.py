"""Generates metadata for Repair Generator rows."""

import hashlib
import json
from typing import Any

from preprocessing.domain.repository import PreprocessedModule
from generators.repair.validation.schema import RepairPayload


def compute_protocol_hash(payload: RepairPayload) -> str:
    """Compute a deterministic SHA256 hash identifying the exact protocol execution logic."""
    canonical_repr = {
        "goal": payload.goal,
        "tasks": sorted(
            [{"id": t.id, "problem": t.problem.description} for t in payload.tasks],
            key=lambda x: x["id"],
        ),
    }
    json_str = json.dumps(canonical_repr, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


def build_metadata(module: PreprocessedModule, protocol_hash: str) -> dict[str, Any]:
    """Compile the metadata dictionary for the JSONL row with full provenance."""
    metadata = {
        "module": module.name,
        "version": module.metadata.get("version", ""),
        "generator": "repair",
        "protocol_hash": protocol_hash,
    }
    return metadata
