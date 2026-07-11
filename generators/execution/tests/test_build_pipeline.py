import unittest
from unittest.mock import Mock
from generators.execution.builders.build_pipeline import BuildPipeline
from generators.execution.builders.build_pipeline_context import (
    BuildPipelineContext,
)


class TestBuildPipeline(unittest.TestCase):
    def test_orchestration(self) -> None:
        executor_mock = Mock()
        pipeline = BuildPipeline(executor=executor_mock)

        ctx_mock = Mock(spec=BuildPipelineContext)
        ctx_mock.builder_registry = Mock()
        ctx_mock.factory_registry = Mock()

        pipeline.execute(ctx_mock)

        ctx_mock.builder_registry.validate.assert_called_once()
        ctx_mock.factory_registry.validate.assert_called_once()
        executor_mock.execute.assert_called_once_with(ctx_mock)


if __name__ == "__main__":
    unittest.main()
