"""Mapper for execution phases."""

from aiodoo_datasets.generators.execution.planning.domain.execution_phase import ExecutionPhase
from aiodoo_datasets.generators.execution.protocol.domain.phase_protocol import PhaseProtocol
from aiodoo_datasets.generators.execution.protocol.mappers.stage_mapper import StageMapper
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext

class PhaseMapper:
    """Maps Planning ExecutionPhase to PhaseProtocol."""
    
    @staticmethod
    def map(phase: ExecutionPhase, context: ProtocolContext) -> PhaseProtocol:
        """Create a PhaseProtocol from an ExecutionPhase."""
        stages = tuple(StageMapper.map(stage, context) for stage in phase.stages)
        context.protocol_statistics.mapped_phases += 1
        return PhaseProtocol(
            phase_id=phase.phase_id,
            name=phase.name,
            stages=stages
        )
