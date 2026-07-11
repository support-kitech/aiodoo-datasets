import unittest
from generators.execution.planning.planning_statistics import PlanningStatistics


class TestPlanningStatistics(unittest.TestCase):
    def test_statistics(self) -> None:
        stats = PlanningStatistics()
        self.assertEqual(stats.stage_count, 0)

        stats.stage_count = 5
        stats.phase_count = 2
        stats.batch_count = 1
        stats.parallel_groups = 0
        stats.execution_depth = 3
        stats.dependency_groups = 1
        stats.critical_path_length = 3

        self.assertEqual(stats.stage_count, 5)
        self.assertEqual(stats.phase_count, 2)
        self.assertEqual(stats.critical_path_length, 3)


if __name__ == "__main__":
    unittest.main()
