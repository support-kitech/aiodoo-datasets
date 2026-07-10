"""Mapper for execution stages."""

from aiodoo_datasets.generators.execution.planning.domain.execution_stage import ExecutionStage
from aiodoo_datasets.generators.execution.protocol.domain.stage_protocol import StageProtocol
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext

class StageMapper:
    """Maps Planning ExecutionStage to StageProtocol."""
    
    @staticmethod
    def map(stage: ExecutionStage, context: ProtocolContext) -> StageProtocol:
        """Create a StageProtocol from an ExecutionStage."""
        nodes = tuple(node.node_id for node in stage.nodes)
        context.protocol_statistics.mapped_stages += 1
        return StageProtocol(
            stage_id=stage.stage_id,
            stage_type=stage.stage_type.value,
            nodes=nodes
        )
