"""Mapper for execution protocol."""

from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)
from aiodoo_datasets.generators.execution.protocol.mappers.schedule_mapper import ScheduleMapper
from aiodoo_datasets.generators.execution.protocol.mappers.metadata_mapper import MetadataMapper
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext
from aiodoo_datasets.generators.execution.protocol.results.mapper_result import MapperResult


class ProtocolMapper:
    """Maps PlannedExecution to ExecutionProtocol."""

    @staticmethod
    def map(context: ProtocolContext) -> MapperResult:
        """Create an ExecutionProtocol from the planning result."""
        planning_result = context.planning_result
        if not planning_result.success or not planning_result.planned_execution:
            return MapperResult(
                success=False,
                diagnostics=("Failed to map protocol due to invalid planning result.",),
            )

        planned_exec = planning_result.planned_execution
        metadata = MetadataMapper.map(context)
        schedules = tuple(
            ScheduleMapper.map(schedule, context) for schedule in planned_exec.schedules
        )

        context.protocol_statistics.mapped_plans += 1

        protocol = ExecutionProtocol(
            plan_id=planned_exec.plan_id,
            graph_id=planned_exec.graph_id,
            metadata=metadata,
            schedules=schedules,
        )

        return MapperResult(success=True, protocol=protocol)
