import hashlib
import json
from typing import Any

from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from aiodoo_datasets.generators.common.discovery.classifier import Scenario
from aiodoo_datasets.generators.planner.validation.schema import PlanPayload
from aiodoo_datasets.generators.common.export.metadata import build_base_metadata

def compute_protocol_hash(module: OdooModule, scenario: Scenario, plan_payload: PlanPayload) -> str:
    """Compute a deterministic SHA256 hash identifying the exact protocol execution logic."""
    core_data = {
        "scenario": scenario.name,
        "goal": plan_payload.goal,
        "module_hash": module.module_hash,
        "manifest_hash": module.manifest_hash,
        "tasks": [t.model_dump() for t in plan_payload.tasks],
    }
    json_str = json.dumps(core_data, sort_keys=True)
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


def build_metadata(module: OdooModule, scenario: Scenario, plan_payload: PlanPayload) -> dict[str, Any]:
    """Compile the metadata dictionary for the JSONL row."""
    metadata = build_base_metadata(module, scenario)
    metadata["protocol_hash"] = compute_protocol_hash(module, scenario, plan_payload)
    return metadata
