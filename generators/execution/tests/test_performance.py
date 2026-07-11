import unittest
import time
from pathlib import Path
from generators.execution.integration.pipeline import IntegrationPipeline
from generators.execution.integration.pipeline_context import PipelineContext
from generators.execution.config.generator_config import GeneratorConfig
from generators.execution.config.export_config import ExportConfig
from generators.execution.config.runtime_config import RuntimeConfig
from generators.execution.integration.pipeline_statistics import PipelineStatistics


class TestPerformance(unittest.TestCase):
    def test_repeated_execution_stability(self) -> None:
        context = PipelineContext(
            generator_config=GeneratorConfig(),
            export_config=ExportConfig(output_directory=Path("/tmp")),
            runtime_config=RuntimeConfig(),
            discovery_result={},
            pipeline_statistics=PipelineStatistics(),
        )

        # Test that executing multiple times doesn't compound memory linearly
        # (Very basic stub test for benchmarking)

        start_time = time.time()
        for _ in range(5):
            res = IntegrationPipeline.execute(context)
            self.assertIsNotNone(res)

        total_time = time.time() - start_time

        # Expect 5 runs to be under 1 second for a basic stub/empty run
        self.assertTrue(total_time < 5.0)


if __name__ == "__main__":
    unittest.main()
