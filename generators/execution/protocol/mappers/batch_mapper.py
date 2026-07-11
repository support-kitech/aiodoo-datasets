"""Mapper for execution batches."""

from generators.execution.planning.domain.execution_batch import ExecutionBatch
from generators.execution.protocol.domain.batch_protocol import BatchProtocol
from generators.execution.protocol.mappers.phase_mapper import PhaseMapper
from generators.execution.protocol.protocol_context import ProtocolContext


class BatchMapper:
    """Maps Planning ExecutionBatch to BatchProtocol."""

    @staticmethod
    def map(batch: ExecutionBatch, context: ProtocolContext) -> BatchProtocol:
        """Create a BatchProtocol from an ExecutionBatch."""
        phases = tuple(PhaseMapper.map(phase, context) for phase in batch.phases)
        context.protocol_statistics.mapped_batches += 1
        return BatchProtocol(batch_id=batch.batch_id, is_parallel=batch.is_parallel, phases=phases)
