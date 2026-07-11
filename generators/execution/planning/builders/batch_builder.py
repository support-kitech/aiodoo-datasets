"""Batch builder."""

from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.results.phase_result import PhaseResult
from aiodoo_datasets.generators.execution.planning.results.batch_result import BatchResult
from aiodoo_datasets.generators.execution.planning.domain.execution_batch import ExecutionBatch


class BatchBuilder:
    """Builder for generating execution batches from phases."""

    @staticmethod
    def build(context: PlanningContext, phase_result: PhaseResult) -> BatchResult:
        """Build batches from generated phases."""
        if not phase_result.success:
            return BatchResult(
                success=False, diagnostics=("Failed to build batches due to invalid phase result.",)
            )

        batch = ExecutionBatch(batch_id="batch_1", is_parallel=False, phases=phase_result.phases)
        context.planning_statistics.batch_count = 1
        return BatchResult(success=True, batches=(batch,))
