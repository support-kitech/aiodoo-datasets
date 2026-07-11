"""Assembles the final Artifact Protocol V1 payload."""

from aiodoo_datasets.generators.coding.discovery import OdooModule, Scenario
from aiodoo_datasets.generators.coding.validation.schema import ArtifactPayload
from aiodoo_datasets.generators.coding.protocol.operation_builder import build_operations
from aiodoo_datasets.generators.coding.protocol.validation_mapper import build_validation_actions

def build_artifact_payload(module: OdooModule, scenario: Scenario, py_k, xml_k, artifacts) -> ArtifactPayload:
    """Orchestrates the protocol payload construction."""
    
    # 2. Build operations
    operations = build_operations(artifacts, py_k, xml_k)
    
    # 3. Build validation hints
    validation_actions = build_validation_actions(artifacts, py_k, xml_k, module)
    
    # Ensure operations are deterministically sorted
    operations.sort(key=lambda o: o.path)
    
    summary = f"Generated {len(artifacts)} artifacts and {len(operations)} operations for {scenario.name}."
    
    payload = ArtifactPayload(
        goal=f"Implement {scenario.name} in {module.name}",
        workspace=f"src/{module.name}",
        artifacts=artifacts,
        operations=operations,
        validation_actions=validation_actions,
        summary=summary
    )
    
    return payload
