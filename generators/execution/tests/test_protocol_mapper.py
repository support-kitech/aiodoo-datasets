import unittest
from types import MappingProxyType
from aiodoo_datasets.generators.execution.protocol.mappers.protocol_mapper import ProtocolMapper
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics
from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult
from aiodoo_datasets.generators.execution.planning.planning_statistics import PlanningStatistics
from aiodoo_datasets.generators.execution.planning.domain.execution_plan import PlannedExecution
from aiodoo_datasets.generators.execution.planning.domain.execution_schedule import (
    ExecutionSchedule,
)
from aiodoo_datasets.generators.execution.planning.domain.execution_batch import ExecutionBatch
from aiodoo_datasets.generators.execution.planning.domain.execution_phase import ExecutionPhase
from aiodoo_datasets.generators.execution.planning.domain.execution_stage import ExecutionStage
from aiodoo_datasets.generators.execution.planning.enums import StageType


class TestProtocolMapper(unittest.TestCase):
    def test_deterministic_mapping(self):
        # Create Planning Domain Objects
        stage = ExecutionStage(stage_id="stg1", stage_type=StageType.EXECUTION, nodes=())
        phase = ExecutionPhase(phase_id="ph1", name="Phase 1", stages=(stage,))
        batch = ExecutionBatch(batch_id="b1", is_parallel=False, phases=(phase,))
        schedule = ExecutionSchedule(schedule_id="sch1", strategy="seq", batches=(batch,))
        plan = PlannedExecution(plan_id="p1", graph_id="g1", schedules=(schedule,))

        planning_result = PlanningResult(success=True, planned_execution=plan)

        ctx = ProtocolContext(
            planning_result=planning_result,
            planning_statistics=PlanningStatistics(),
            configuration=MappingProxyType({}),
            protocol_version="1.0.0",
            protocol_statistics=ProtocolStatistics(),
        )

        res = ProtocolMapper.map(ctx)
        self.assertTrue(res.success)
        self.assertIsNotNone(res.protocol)

        # Verify deterministic mapping structure
        protocol = res.protocol
        self.assertEqual(protocol.plan_id, "p1")
        self.assertEqual(protocol.graph_id, "g1")
        self.assertEqual(len(protocol.schedules), 1)
        self.assertEqual(protocol.schedules[0].schedule_id, "sch1")
        self.assertEqual(protocol.schedules[0].batches[0].batch_id, "b1")


if __name__ == "__main__":
    unittest.main()
