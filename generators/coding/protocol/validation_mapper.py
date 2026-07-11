"""Generates expected validation actions for the Artifact Protocol."""

from aiodoo_datasets.generators.coding.validation.schema import ValidationAction, GeneratedArtifact

from aiodoo_datasets.generators.coding.discovery import PythonKnowledge, XMLKnowledge, OdooModule


def build_validation_actions(
    artifacts: list[GeneratedArtifact],
    py_k: PythonKnowledge,
    xml_k: XMLKnowledge,
    module: OdooModule,
) -> list[ValidationAction]:
    """
    Determines necessary execution hints for AIODOO Core based on generated artifacts.
    Generates validation hints from engineering analysis.
    """
    actions = []

    # Analyze Python models
    for py_file, k in py_k.files.items():
        if k.models:
            for model_name, model_def in k.models.items():
                if model_def.inherit and not model_def.name:
                    actions.append(
                        ValidationAction(
                            action="Check Model Extension",
                            reason=f"Verify extension of '{model_def.inherit[0]}' is syntactically valid.",
                        )
                    )
                else:
                    actions.append(
                        ValidationAction(
                            action="Check Model Registration",
                            reason=f"Verify new model '{model_name}' registers correctly in registry.",
                        )
                    )

    # Analyze XML views
    for xml_file, k in xml_k.files.items():
        if k.views:
            for view in k.views:
                if getattr(view, "inherit_id", None):
                    actions.append(
                        ValidationAction(
                            action="Check View Inheritance",
                            reason=f"Verify parent view '{view.inherit_id}' exists and xpath expressions apply correctly.",
                        )
                    )

    # Manifest validation
    if module.manifest.depends:
        actions.append(
            ValidationAction(
                action="Check Dependencies",
                reason=f"Verify manifest dependencies {module.manifest.depends} are satisfied.",
            )
        )

    has_python = any(a.path.endswith(".py") and "__manifest__.py" not in a.path for a in artifacts)
    has_xml = any(a.path.endswith(".xml") for a in artifacts)

    if has_python:
        actions.append(
            ValidationAction(
                action="Restart Odoo", reason="Python logic modified, requires server restart."
            )
        )

    if has_xml:
        actions.append(
            ValidationAction(
                action="Update Module", reason="XML logic modified, requires UI update."
            )
        )

    # Sort for determinism
    actions.sort(key=lambda a: (a.action, a.reason))

    return actions
