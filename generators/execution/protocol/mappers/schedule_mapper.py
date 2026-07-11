"""Mapper for execution schedules."""

from generators.execution.planning.domain.execution_schedule import (
    ExecutionSchedule,
)
from generators.execution.protocol.domain.schedule_protocol import ScheduleProtocol
from generators.execution.protocol.mappers.batch_mapper import BatchMapper
from generators.execution.protocol.protocol_context import ProtocolContext


class ScheduleMapper:
    """Maps Planning ExecutionSchedule to ScheduleProtocol."""

    @staticmethod
    def map(schedule: ExecutionSchedule, context: ProtocolContext) -> ScheduleProtocol:
        """Create a ScheduleProtocol from an ExecutionSchedule."""
        batches = tuple(BatchMapper.map(batch, context) for batch in schedule.batches)
        context.protocol_statistics.mapped_schedules += 1
        return ScheduleProtocol(
            schedule_id=schedule.schedule_id, strategy=schedule.strategy, batches=batches
        )
