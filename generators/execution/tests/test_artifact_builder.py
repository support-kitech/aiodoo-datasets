import unittest
from unittest.mock import Mock
from aiodoo_datasets.generators.execution.builders.artifact_builder import ArtifactBuilder
from aiodoo_datasets.generators.execution.builders.results.artifact_build_result import (
    ArtifactBuildResult,
)


class TestArtifactBuilder(unittest.TestCase):
    def test_build_signature(self):
        builder = ArtifactBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, ArtifactBuildResult)


if __name__ == "__main__":
    unittest.main()
