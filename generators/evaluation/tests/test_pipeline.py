"""Pipeline Integration Tests for Evaluation Generator."""

import unittest
from aiodoo_datasets.generators.evaluation import api


class TestEvaluationPipeline(unittest.TestCase):
    """Verifies complete integration flow."""

    def test_end_to_end_generate(self) -> None:
        """Verify the pipeline generates a valid dataset."""
        config = {"benchmark_name": "IntegrationBench", "evaluation_type": "logic"}

        result = api.generate(config)

        # Validate output structures
        self.assertTrue(result.validation_passed)
        self.assertEqual(len(result.dataset), 1)
        self.assertEqual(result.dataset[0].catalog.catalog_name, "IntegrationBench")


if __name__ == "__main__":
    unittest.main()
