import unittest
from pathlib import Path
from generators.execution.integration.pipeline import IntegrationPipeline
from generators.execution.integration.pipeline_context import PipelineContext
from generators.execution.config.generator_config import GeneratorConfig
from generators.execution.config.export_config import ExportConfig
from generators.execution.config.runtime_config import RuntimeConfig
from generators.execution.integration.pipeline_statistics import PipelineStatistics


class TestIntegrationPipeline(unittest.TestCase):
    def test_pipeline_execution(self) -> None:
        context = PipelineContext(
            generator_config=GeneratorConfig(),
            export_config=ExportConfig(output_directory=Path("/tmp")),
            runtime_config=RuntimeConfig(),
            discovery_result={},
            pipeline_statistics=PipelineStatistics(),
        )

        result = IntegrationPipeline.execute(context)

        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIsNotNone(result.statistics)


if __name__ == "__main__":
    unittest.main()
