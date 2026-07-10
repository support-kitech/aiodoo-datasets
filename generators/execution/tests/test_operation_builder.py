import unittest
from unittest.mock import Mock
from aiodoo_datasets.generators.execution.builders.operation_builder import OperationBuilder
from aiodoo_datasets.generators.execution.builders.results.operation_build_result import OperationBuildResult

class TestOperationBuilder(unittest.TestCase):
    def test_build_signature(self):
        builder = OperationBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, OperationBuildResult)

if __name__ == '__main__':
    unittest.main()
