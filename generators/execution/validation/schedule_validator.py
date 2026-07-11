"""Schedule validator."""

from aiodoo_datasets.generators.execution.planning.domain.execution_schedule import (
    ExecutionSchedule,
)
from aiodoo_datasets.generators.execution.validation.batch_validator import BatchValidator


class ScheduleValidator:
    """Validator for execution schedules."""

    @staticmethod
    def validate(schedule: ExecutionSchedule) -> tuple[str, ...]:
        """Validate a schedule and its batches."""
        violations = []
        if not schedule.schedule_id:
            violations.append("Schedule has no schedule_id.")
        if not schedule.batches:
            violations.append(f"Schedule {schedule.schedule_id} has no batches.")

        for batch in schedule.batches:
            violations.extend(BatchValidator.validate(batch))

        return tuple(violations)
