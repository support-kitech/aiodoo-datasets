"""Generates metadata for Coding Generator rows."""

import hashlib
import json
from typing import Any

from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from aiodoo_datasets.generators.common.discovery.classifier import Scenario
from aiodoo_datasets.generators.coding.validation.schema import ArtifactPayload
from aiodoo_datasets.generators.common.export.metadata import build_base_metadata


def compute_protocol_hash(module: OdooModule, scenario: Scenario, payload: ArtifactPayload) -> str:
    """Compute a deterministic SHA256 hash identifying the exact protocol execution logic."""
    canonical_repr = {
        "goal": payload.goal,
        "workspace": payload.workspace,
        "artifacts": sorted(
            [
                {
                    "id": a.id,
                    "type": a.type,
                    "path": a.path,
                    "intent": a.intent,
                    "deps": sorted(a.dependencies),
                }
                for a in payload.artifacts
            ],
            key=lambda x: x["path"],
        ),
        "operations": sorted(
            [{"op": o.operation, "path": o.path} for o in payload.operations],
            key=lambda x: x["path"],
        ),
        "validations": sorted(
            [{"action": v.action, "reason": v.reason} for v in payload.validation_actions],
            key=lambda x: (x["action"], x["reason"]),
        ),
    }
    json_str = json.dumps(canonical_repr, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


def build_metadata(
    module: OdooModule, scenario: Scenario, payload: ArtifactPayload
) -> dict[str, Any]:
    """Compile the metadata dictionary for the JSONL row with full provenance."""
    metadata = build_base_metadata(module, scenario)
    metadata["protocol_hash"] = compute_protocol_hash(module, scenario, payload)
    return metadata
