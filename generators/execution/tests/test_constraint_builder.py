import unittest
from unittest.mock import Mock
from aiodoo_datasets.generators.execution.builders.constraint_builder import ConstraintBuilder
from aiodoo_datasets.generators.execution.builders.results.constraint_build_result import (
    ConstraintBuildResult,
)


class TestConstraintBuilder(unittest.TestCase):
    def test_build_signature(self):
        builder = ConstraintBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, ConstraintBuildResult)


if __name__ == "__main__":
    unittest.main()
