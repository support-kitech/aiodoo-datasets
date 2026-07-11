import unittest
from unittest.mock import Mock
from generators.execution.builders.artifact_builder import ArtifactBuilder
from generators.execution.builders.results.artifact_build_result import (
    ArtifactBuildResult,
)


class TestArtifactBuilder(unittest.TestCase):
    def test_build_signature(self) -> None:
        builder = ArtifactBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, ArtifactBuildResult)


if __name__ == "__main__":
    unittest.main()
