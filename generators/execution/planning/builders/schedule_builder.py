"""Schedule builder."""

from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.results.batch_result import BatchResult
from generators.execution.planning.results.schedule_result import ScheduleResult
from generators.execution.planning.domain.execution_schedule import (
    ExecutionSchedule,
)


class ScheduleBuilder:
    """Builder for generating execution schedules from batches."""

    @staticmethod
    def build(context: PlanningContext, batch_result: BatchResult) -> ScheduleResult:
        """Build schedules from generated batches."""
        if not batch_result.success:
            return ScheduleResult(
                success=False,
                diagnostics=("Failed to build schedules due to invalid batch result.",),
            )

        schedule = ExecutionSchedule(
            schedule_id="schedule_1", strategy=context.strategy.value, batches=batch_result.batches
        )
        return ScheduleResult(success=True, schedules=(schedule,))
