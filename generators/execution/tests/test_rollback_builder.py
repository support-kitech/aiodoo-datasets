import unittest
from unittest.mock import Mock
from aiodoo_datasets.generators.execution.builders.rollback_builder import RollbackBuilder
from aiodoo_datasets.generators.execution.builders.results.rollback_build_result import (
    RollbackBuildResult,
)


class TestRollbackBuilder(unittest.TestCase):
    def test_build_signature(self) -> None:
        builder = RollbackBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, RollbackBuildResult)


if __name__ == "__main__":
    unittest.main()
