"""Planner orchestrator."""

from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.planning_result import PlanningResult
from generators.execution.planning.builders.stage_builder import StageBuilder
from generators.execution.planning.builders.phase_builder import PhaseBuilder
from generators.execution.planning.builders.batch_builder import BatchBuilder
from generators.execution.planning.builders.schedule_builder import ScheduleBuilder
from generators.execution.planning.domain.execution_plan import PlannedExecution


class Planner:
    """
    Orchestrates the planning pipeline:
    Validated Graph -> Stage Builder -> Phase Builder -> Batch Builder -> Schedule Builder
    """

    @staticmethod
    def plan(context: PlanningContext) -> PlanningResult:
        """Execute the planning pipeline."""

        # 1. Build Stages
        stage_result = StageBuilder.build(context)
        if not stage_result.success:
            return PlanningResult(success=False, diagnostics=stage_result.diagnostics)

        # 2. Build Phases
        phase_result = PhaseBuilder.build(context, stage_result)
        if not phase_result.success:
            return PlanningResult(success=False, diagnostics=phase_result.diagnostics)

        # 3. Build Batches
        batch_result = BatchBuilder.build(context, phase_result)
        if not batch_result.success:
            return PlanningResult(success=False, diagnostics=batch_result.diagnostics)

        # 4. Build Schedules
        schedule_result = ScheduleBuilder.build(context, batch_result)
        if not schedule_result.success:
            return PlanningResult(success=False, diagnostics=schedule_result.diagnostics)

        # 5. Assemble PlannedExecution
        planned_execution = PlannedExecution(
            plan_id="plan_1",  # Placeholder ID, would normally use hashing or context
            graph_id=context.graph.graph_id if hasattr(context.graph, "graph_id") else "graph_1",
            schedules=schedule_result.schedules,
        )

        return PlanningResult(success=True, planned_execution=planned_execution)
