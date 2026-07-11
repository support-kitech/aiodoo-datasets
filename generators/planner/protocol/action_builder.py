"""Generates Protocol V1 PlanAction objects."""

from generators.planner.validation.schema import TaskSpec, PlanAction


def build_actions(tasks: list[TaskSpec]) -> list[PlanAction]:
    """Derive executable actions from the defined tasks, mirroring dependencies."""
    actions = []
    for task in tasks:
        # For datasets, we simulate the high-level commands
        action_type = "create_file"
        if "Extend" in task.title or "Configure" in task.title:
            action_type = "update_file"

        actions.append(
            PlanAction(
                id=f"act_{task.id}",
                action=action_type,
                args={"target": "src/odoo_module"},
                reason=f"Execute {task.title}",
                expected_result="File generated successfully.",
                depends_on=[f"act_{dep}" for dep in task.dependencies],
                continue_on_error=False,
            )
        )
    return actions
