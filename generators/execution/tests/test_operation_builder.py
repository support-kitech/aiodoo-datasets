import unittest
from unittest.mock import Mock
from generators.execution.builders.operation_builder import OperationBuilder
from generators.execution.builders.results.operation_build_result import (
    OperationBuildResult,
)


class TestOperationBuilder(unittest.TestCase):
    def test_build_signature(self) -> None:
        builder = OperationBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, OperationBuildResult)


if __name__ == "__main__":
    unittest.main()
