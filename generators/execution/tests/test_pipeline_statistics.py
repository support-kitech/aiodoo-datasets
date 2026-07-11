import unittest
from aiodoo_datasets.generators.execution.integration.pipeline_statistics import PipelineStatistics


class TestPipelineStatistics(unittest.TestCase):
    def test_statistics_initialization(self) -> None:
        stats = PipelineStatistics()
        self.assertEqual(stats.total_execution_time, 0.0)
        self.assertEqual(stats.generated_records, 0)
        self.assertEqual(stats.validation_failures, 0)

    def test_statistics_mutation(self) -> None:
        stats = PipelineStatistics()
        stats.total_execution_time = 5.0
        stats.phase_execution_times["ANALYSIS"] = 2.0
        self.assertEqual(stats.total_execution_time, 5.0)
        self.assertEqual(stats.phase_execution_times["ANALYSIS"], 2.0)


if __name__ == "__main__":
    unittest.main()
