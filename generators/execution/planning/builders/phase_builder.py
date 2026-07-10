"""Phase builder."""

from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.results.stage_result import StageResult
from aiodoo_datasets.generators.execution.planning.results.phase_result import PhaseResult
from aiodoo_datasets.generators.execution.planning.domain.execution_phase import ExecutionPhase

class PhaseBuilder:
    """Builder for generating execution phases from stages."""
    
    @staticmethod
    def build(context: PlanningContext, stage_result: StageResult) -> PhaseResult:
        """Build phases from generated stages."""
        if not stage_result.success:
            return PhaseResult(success=False, diagnostics=("Failed to build phases due to invalid stage result.",))
            
        phase = ExecutionPhase(
            phase_id="phase_1",
            name="Main Phase",
            stages=stage_result.stages
        )
        context.planning_statistics.phase_count = 1
        return PhaseResult(success=True, phases=(phase,))
