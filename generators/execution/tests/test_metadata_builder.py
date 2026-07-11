import unittest
from unittest.mock import Mock
from generators.execution.builders.metadata_builder import MetadataBuilder
from generators.execution.builders.results.metadata_build_result import (
    MetadataBuildResult,
)


class TestMetadataBuilder(unittest.TestCase):
    def test_build_signature(self) -> None:
        builder = MetadataBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, MetadataBuildResult)


if __name__ == "__main__":
    unittest.main()
