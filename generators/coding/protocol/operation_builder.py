"""Generates file operations matching AIODOO Protocol V1."""

from aiodoo_datasets.generators.coding.discovery import PythonKnowledge, XMLKnowledge
from aiodoo_datasets.generators.coding.validation.schema import FileOperation, GeneratedArtifact


def build_operations(
    artifacts: list[GeneratedArtifact], py_k: PythonKnowledge, xml_k: XMLKnowledge
) -> list[FileOperation]:
    """
    Translates generated artifacts into actionable file operations.
    Operation inference is based on engineering analysis rather than assumptions.
    """
    operations = []

    for artifact in artifacts:
        op_type = "CREATE"
        path = artifact.path

        # Determine from Metadata / AST Knowledge where possible
        if path.endswith(".py") and path in py_k.files:
            file_info = py_k.files[path]

            # Python models
            if file_info.models:
                is_update = False
                for model_name, model_def in file_info.models.items():
                    if model_def.inherit and not model_def.name:
                        is_update = True
                    elif model_def.inherit and model_name in model_def.inherit:
                        is_update = True
                if is_update:
                    op_type = "UPDATE"

            # Controllers
            elif hasattr(file_info, "controllers") and file_info.controllers:
                op_type = "UPDATE"

            # Manifest
            elif (
                "depends" in getattr(file_info, "manifest", {})
                or path.endswith("__manifest__.py")
                or path.endswith("__openerp__.py")
            ):
                op_type = "UPDATE"

        elif path.endswith(".xml") and path in xml_k.files:
            file_info = xml_k.files[path]
            is_patch = False

            # Views
            for view in file_info.views:
                if getattr(view, "inherit_id", None):
                    is_patch = True
                    break

            # Actions and Menus usually modify UI trees
            if (
                not is_patch
                and hasattr(file_info, "tags")
                and any("menuitem" in t or "act_window" in t for t in file_info.tags)
            ):
                is_patch = True

            # Report definitions create new reports
            is_report = hasattr(file_info, "tags") and any("report" in t for t in file_info.tags)

            # Assets usually update existing web bundles
            is_asset = hasattr(file_info, "tags") and any("assets" in t for t in file_info.tags)

            if is_patch:
                op_type = "PATCH"
            elif is_asset:
                op_type = "UPDATE"
            elif is_report:
                op_type = "CREATE"
            else:
                op_type = "CREATE"

        elif path.endswith(".csv"):
            if "security" in path or "ir.model.access" in path:
                op_type = "PATCH"
            else:
                op_type = "CREATE"

        op = FileOperation(
            operation=op_type, path=artifact.path, intent=artifact.intent, reason=artifact.reason
        )
        operations.append(op)

    return operations
