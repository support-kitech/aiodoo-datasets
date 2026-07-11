"""Generates instructions for the dataset row."""

from preprocessing.domain.repository import PreprocessedModule
from generators.repair.analysis.rules.base import RepairOpportunity


def generate_instruction(module: PreprocessedModule, opportunities: list[RepairOpportunity]) -> str:
    """Generate the user-facing prompt that initiates the repair."""
    issues = ", ".join(set(o.problem_description for o in opportunities))
    return (
        f"Please analyze and repair the {len(opportunities)} identified issues in the `{module.name}` module. "
        f"Known issues include: {issues}. "
        f"Ensure you follow modern Odoo standards and preserve existing business logic."
    )
