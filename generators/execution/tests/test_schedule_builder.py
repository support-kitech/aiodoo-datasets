import unittest
from aiodoo_datasets.generators.execution.planning.builders.stage_builder import StageBuilder
from aiodoo_datasets.generators.execution.planning.builders.phase_builder import PhaseBuilder
from aiodoo_datasets.generators.execution.planning.builders.batch_builder import BatchBuilder
from aiodoo_datasets.generators.execution.planning.builders.schedule_builder import ScheduleBuilder
from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.planning_statistics import PlanningStatistics
from aiodoo_datasets.generators.execution.planning.enums import PlanningStrategyType
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.enums import NodeType
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics
from types import MappingProxyType


class TestScheduleBuilder(unittest.TestCase):
    def test_schedule_generation(self) -> None:
        n1 = ExecutionNode(node_id="a", node_type=NodeType.STEP, payload="p")
        g = ExecutionGraph(nodes=(n1,), edges=())
        g_stats = GraphStatistics()
        p_stats = PlanningStatistics()

        ctx = PlanningContext(
            graph=g,
            graph_statistics=g_stats,
            configuration=MappingProxyType({}),
            strategy=PlanningStrategyType.SEQUENTIAL,
            planning_statistics=p_stats,
        )

        s_res = StageBuilder.build(ctx)
        p_res = PhaseBuilder.build(ctx, s_res)
        b_res = BatchBuilder.build(ctx, p_res)
        sch_res = ScheduleBuilder.build(ctx, b_res)
        self.assertTrue(sch_res.success)
        self.assertEqual(len(sch_res.schedules), 1)


if __name__ == "__main__":
    unittest.main()
