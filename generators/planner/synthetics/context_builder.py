"""Builds minimal input context for the Planner model."""

from preprocessing.domain.repository import PreprocessedModule


def build_context(module: PreprocessedModule) -> str:
    """Generates the minimal realistic input context."""
    depends = ", ".join(module.metadata.get("depends", [])) or "base"
    return f"Target Odoo Version: {module.metadata.get('version', '')}\\nAvailable Dependencies: {depends}"
