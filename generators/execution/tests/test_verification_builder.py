import unittest
from unittest.mock import Mock
from aiodoo_datasets.generators.execution.builders.verification_builder import VerificationBuilder
from aiodoo_datasets.generators.execution.builders.results.verification_build_result import VerificationBuildResult

class TestVerificationBuilder(unittest.TestCase):
    def test_build_signature(self):
        builder = VerificationBuilder()
        ctx = Mock()
        ctx.statistics = Mock()
        result = builder.build(ctx)
        self.assertIsInstance(result, VerificationBuildResult)

if __name__ == '__main__':
    unittest.main()
