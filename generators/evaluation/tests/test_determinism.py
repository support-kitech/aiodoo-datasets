"""Determinism Tests for Evaluation Generator."""

import unittest
from aiodoo_datasets.generators.evaluation import api

class TestEvaluationDeterminism(unittest.TestCase):
    """Verifies complete deterministic behavior of the pipeline."""
    
    def test_pipeline_determinism(self):
        """Run identical input multiple times and verify byte-for-byte identical output."""
        config = {
            "evaluation_type": "coding",
            "target_generator": "coding_generator",
            "benchmark_name": "TestBench",
            "benchmark_category": "tests",
            "source_protocols": {
                "coding": {"dummy": "data"} # Simulate protocol struct
            }
        }
        
        # Run 1
        result1 = api.generate(config)
        dataset1_dump = [proto.model_dump() for proto in result1.dataset]
        stats1_dump = dict(result1.statistics)
        
        # Run 2
        result2 = api.generate(config)
        dataset2_dump = [proto.model_dump() for proto in result2.dataset]
        stats2_dump = dict(result2.statistics)
        
        # Verify deterministic IDs, orderings, and content
        self.assertEqual(dataset1_dump, dataset2_dump)
        self.assertEqual(stats1_dump, stats2_dump)

if __name__ == "__main__":
    unittest.main()
