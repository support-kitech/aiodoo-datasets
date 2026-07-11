import unittest
from aiodoo_datasets.generators.execution.planning.builders.stage_builder import StageBuilder
from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.planning_statistics import PlanningStatistics
from aiodoo_datasets.generators.execution.planning.enums import PlanningStrategyType
from aiodoo_datasets.generators.execution.graph.graph import ExecutionGraph
from aiodoo_datasets.generators.execution.graph.node import ExecutionNode
from aiodoo_datasets.generators.execution.graph.enums import NodeType
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics
from types import MappingProxyType


class TestStageBuilder(unittest.TestCase):
    def test_stage_generation(self) -> None:
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

        res = StageBuilder.build(ctx)
        self.assertTrue(res.success)
        self.assertEqual(len(res.stages), 1)


if __name__ == "__main__":
    unittest.main()
