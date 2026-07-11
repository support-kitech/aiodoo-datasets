import unittest
from generators.execution.planning.builders.stage_builder import StageBuilder
from generators.execution.planning.builders.phase_builder import PhaseBuilder
from generators.execution.planning.builders.batch_builder import BatchBuilder
from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.planning_statistics import PlanningStatistics
from generators.execution.planning.enums import PlanningStrategyType
from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.node import ExecutionNode
from generators.execution.graph.enums import NodeType
from generators.execution.graph.statistics import GraphStatistics
from types import MappingProxyType


class TestBatchBuilder(unittest.TestCase):
    def test_batch_generation(self) -> None:
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
        self.assertTrue(b_res.success)
        self.assertEqual(len(b_res.batches), 1)


if __name__ == "__main__":
    unittest.main()
