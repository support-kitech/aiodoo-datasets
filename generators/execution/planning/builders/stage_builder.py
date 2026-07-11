"""Stage builder."""

from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.results.stage_result import StageResult
from generators.execution.planning.domain.execution_stage import ExecutionStage
from generators.execution.planning.enums import StageType


class StageBuilder:
    """Builder for generating execution stages."""

    @staticmethod
    def build(context: PlanningContext) -> StageResult:
        """
        Build stages from the execution graph.
        For simplicity, this groups all nodes into a single EXECUTION stage.
        A more advanced strategy would group nodes based on dependencies or configuration.
        """
        # In a real implementation, this would use the strategy to partition nodes.
        # For now, deterministic simple grouping.
        if context.graph is None:
            return StageResult(success=False, diagnostics=("No valid execution graph provided.",))

        nodes = context.graph.nodes
        if not nodes:
            return StageResult(success=False, diagnostics=("Graph contains no nodes.",))
        stage = ExecutionStage(
            stage_id=f"stage_{context.graph_statistics.node_count}",
            stage_type=StageType.EXECUTION,
            nodes=nodes,
        )
        context.planning_statistics.stage_count = 1
        return StageResult(success=True, stages=(stage,))
