"""Maps raw extracted implementation data into Artifact Protocol objects."""

import hashlib
from aiodoo_datasets.generators.coding.validation.schema import GeneratedArtifact


def map_to_artifact(
    raw_data: dict, dependencies: list[str], module_version: str, module_name: str  # type: ignore[type-arg]
) -> GeneratedArtifact:
    """Translates raw file data into a strictly typed GeneratedArtifact with deterministic ID."""

    # Deterministic ID generation based on stable inputs
    seed_str = f"{module_version}_{module_name}_file_{raw_data['path']}"
    stable_id = f"art_{hashlib.sha256(seed_str.encode('utf-8')).hexdigest()[:12]}"

    # Convert structured intent dict to string for final schema
    intent_dict = raw_data.get("intent", {})
    if isinstance(intent_dict, dict):
        intent_parts = []
        if intent_dict.get("purpose"):
            intent_parts.append(f"Purpose: {intent_dict['purpose']}")
        if intent_dict.get("targets"):
            intent_parts.append(f"Targets: {', '.join(intent_dict['targets'])}")
        if intent_dict.get("constraints"):
            intent_parts.append(f"Constraints: {', '.join(intent_dict['constraints'])}")
        if intent_dict.get("dependencies"):
            intent_parts.append(f"Dependencies: {', '.join(intent_dict['dependencies'])}")
        intent_str = " | ".join(intent_parts) if intent_parts else "Implement engineering logic"
    else:
        intent_str = str(intent_dict)

    return GeneratedArtifact(
        id=stable_id,
        type="file",
        language=raw_data["lang"],
        path=raw_data["path"],
        intent=intent_str,
        reason=f"Implement {raw_data['path']} for {raw_data.get('scenario_name', 'feature')}",
        created_by="aiodoo_coding_model",
        dependencies=sorted(dependencies),
        validation_status="validated",
    )
