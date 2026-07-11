"""Reverse-engineers real Odoo files into Artifact Protocol objects."""

from preprocessing.domain.repository import PreprocessedModule
from generators.coding.discovery import (
    Scenario,
    PythonKnowledge,
    XMLKnowledge,
)
from generators.coding.validation.schema import GeneratedArtifact
from generators.coding.generation.dependency_builder import determine_dependencies


def build_artifacts(
    module: PreprocessedModule, scenario: Scenario, py_k: PythonKnowledge, xml_k: XMLKnowledge
) -> list[GeneratedArtifact]:
    """
    Slices the real Odoo codebase into discrete GeneratedArtifacts based on the scenario.
    """
    artifacts = []

    # We collect all raw files that belong to the scenario.
    # For a perfect slice, we would ideally filter by AST/XML tags matching the scenario.
    # Here we simulate the extraction of files related to the module.
    raw_files = []

    for py_file, k in py_k.files.items():
        if scenario.name in [m.name for m in k.models.values()] or len(scenario.tags) > 0:
            raw_files.append((py_file, "python"))

    for xml_file, k in xml_k.files.items():
        if scenario.name in [v.model for v in k.views if v.model] or len(scenario.tags) > 0:
            raw_files.append((xml_file, "xml"))

    # Include manifest
    from pathlib import Path

    module_path = Path(str(module.metadata["path"]))
    manifest_path = (
        "__manifest__.py" if (module_path / "__manifest__.py").exists() else "__openerp__.py"
    )
    raw_files.append((manifest_path, "python"))

    # To avoid duplicates in raw_files
    raw_files = list(set(raw_files))

    # Temporarily store to resolve dependencies
    temp_artifacts = []
    for idx, (rel_path, lang) in enumerate(raw_files):
        # We no longer read raw file content from disk to embed in artifacts

        intent = {
            "purpose": f"Implement engineering logic for {rel_path}",
            "targets": [],
            "constraints": [],
            "dependencies": [],
        }

        if lang == "python" and rel_path in py_k.files:
            file_info = py_k.files[rel_path]
            if file_info.models:
                models = [m.name for m in file_info.models.values()]
                intent["targets"].extend([f"Model: {m}" for m in models])  # type: ignore[attr-defined]
                intent["purpose"] = f"Backend logic and data models for {', '.join(models)}"
            if hasattr(file_info, "controllers") and file_info.controllers:
                intent["targets"].append("Controller routes")  # type: ignore[attr-defined]
                intent["purpose"] = "Define web controller endpoints"

        elif lang == "xml" and rel_path in xml_k.files:
            file_info = xml_k.files[rel_path]
            if file_info.views:
                models_viewed = sorted(list(set([v.model for v in file_info.views if v.model])))
                if models_viewed:
                    intent["targets"].extend([f"View for model: {m}" for m in models_viewed])  # type: ignore[attr-defined]
                    intent["purpose"] = f"User interface views for {', '.join(models_viewed)}"

        # Do NOT embed raw source code, only engineering intent!

        ta = {"path": rel_path, "intent": intent, "lang": lang, "scenario_name": scenario.name}
        temp_artifacts.append(ta)

    from generators.coding.protocol.artifact_mapper import map_to_artifact

    for ta in temp_artifacts:
        deps = determine_dependencies(ta["path"], temp_artifacts, py_k, xml_k, module)

        art = map_to_artifact(
            raw_data=ta,
            dependencies=deps,
            module_version=str(module.metadata["version"]),
            module_name=module.name,
        )
        artifacts.append(art)

    # Sort artifacts for deterministic stability
    artifacts.sort(key=lambda a: a.path)

    return artifacts
