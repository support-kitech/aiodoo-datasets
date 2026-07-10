"""Stage builder."""

from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.results.stage_result import StageResult
from aiodoo_datasets.generators.execution.planning.domain.execution_stage import ExecutionStage
from aiodoo_datasets.generators.execution.planning.enums import StageType

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
        nodes = context.graph.nodes
        stage = ExecutionStage(
            stage_id=f"stage_{context.graph_statistics.node_count}",
            stage_type=StageType.EXECUTION,
            nodes=nodes
        )
        context.planning_statistics.stage_count = 1
        return StageResult(success=True, stages=(stage,))
