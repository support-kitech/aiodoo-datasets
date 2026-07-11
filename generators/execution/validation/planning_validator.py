"""Planning validator."""

from aiodoo_datasets.generators.execution.planning.domain.execution_plan import PlannedExecution
from aiodoo_datasets.generators.execution.validation.schedule_validator import ScheduleValidator


class PlanningValidator:
    """Orchestrates validation of the entire planned execution."""

    @staticmethod
    def validate(plan: PlannedExecution) -> tuple[str, ...]:
        """Validate the full planned execution."""
        violations = []
        if not plan.plan_id:
            violations.append("PlannedExecution has no plan_id.")
        if not plan.schedules:
            violations.append(f"PlannedExecution {plan.plan_id} has no schedules.")

        for schedule in plan.schedules:
            violations.extend(ScheduleValidator.validate(schedule))

        return tuple(violations)
