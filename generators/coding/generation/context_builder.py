"""Builds minimal context required for the Coding Model implementation."""

from typing import Any
from generators.coding.discovery import (
    OdooModule,
    Scenario,
    PythonKnowledge,
    XMLKnowledge,
)

from generators.coding.validation.schema import ArtifactPayload


def build_context(
    module: OdooModule,
    scenario: Scenario,
    py_k: PythonKnowledge,
    xml_k: XMLKnowledge,
    payload: ArtifactPayload,
) -> dict[str, Any]:
    """
    Extracts minimal related codebase context.
    Never returns the entire source code of the module, just dependencies and structural hints.
    """
    target_artifacts = [a.path for a in payload.artifacts]

    context = {
        "module": module.name,
        "version": module.version,
        "depends": module.manifest.depends,
        "scenario": scenario.name,
        "existing_models": [],
        "existing_views": [],
        "target_artifact": target_artifacts,
        "existing_artifact_names": list(py_k.files.keys()) + list(xml_k.files.keys()),
    }

    # We provide a shallow map of what already exists so the model knows what it's extending
    for py_file, file_knowledge in py_k.files.items():
        if file_knowledge.models:
            context["existing_models"].extend([m.name for m in file_knowledge.models.values()])

    for xml_file, file_knowledge in xml_k.files.items():
        if file_knowledge.views:
            context["existing_views"].extend([v.model for v in file_knowledge.views if v.model])

    # Deduplicate lists
    context["existing_models"] = list(set(context["existing_models"]))
    context["existing_views"] = list(set(context["existing_views"]))

    return context
