"""Builds minimal input context for the Planner model."""

from aiodoo_datasets.generators.planner.discovery.scanner import OdooModule


def build_context(module: OdooModule) -> str:
    """Generates the minimal realistic input context."""
    depends = ", ".join(module.manifest.depends) or "base"
    return f"Target Odoo Version: {module.version}\\nAvailable Dependencies: {depends}"
