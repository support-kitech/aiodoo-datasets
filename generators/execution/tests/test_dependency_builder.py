import unittest
from unittest.mock import Mock
from generators.execution.builders.dependency_builder import DependencyBuilder
from generators.execution.builders.results.dependency_build_result import (
    DependencyBuildResult,
)


class TestDependencyBuilder(unittest.TestCase):
    def test_build_signature(self) -> None:
        builder = DependencyBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, DependencyBuildResult)


if __name__ == "__main__":
    unittest.main()
