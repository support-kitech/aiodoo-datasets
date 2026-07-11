import hashlib
import json
from typing import Any

from preprocessing.domain.repository import PreprocessedModule
from generators.common.discovery.classifier import Scenario
from generators.planner.validation.schema import PlanPayload
from generators.common.export.metadata import build_base_metadata


def compute_protocol_hash(module: PreprocessedModule, scenario: Scenario, plan_payload: PlanPayload) -> str:
    """Compute a deterministic SHA256 hash identifying the exact protocol execution logic."""
    core_data = {
        "scenario": scenario.name,
        "goal": plan_payload.goal,
        "module_hash": "",
        "manifest_hash": "",
        "tasks": [t.model_dump() for t in plan_payload.tasks],
    }
    json_str = json.dumps(core_data, sort_keys=True)
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


def build_metadata(
    module: PreprocessedModule, scenario: Scenario, protocol_hash: str
) -> dict[str, Any]:
    """Compile the metadata dictionary for the JSONL row."""
    metadata = build_base_metadata(module, scenario)
    metadata["protocol_hash"] = protocol_hash
    return metadata  # type: ignore[no-any-return]
