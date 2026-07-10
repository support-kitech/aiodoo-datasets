import unittest
from unittest.mock import Mock
from aiodoo_datasets.generators.execution.builders.pipeline_executor import PipelineExecutor
from aiodoo_datasets.generators.execution.builders.build_pipeline_context import BuildPipelineContext

class TestPipelineExecutor(unittest.TestCase):
    
    def test_executor_empty(self):
        executor = PipelineExecutor()
        ctx_mock = Mock(spec=BuildPipelineContext)
        ctx_mock.builder_registry = Mock()
        ctx_mock.builder_registry.items.return_value = ()
        ctx_mock.builder_context = Mock()
        ctx_mock.diagnostics = Mock()
        
        result = executor.execute(ctx_mock)
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()
