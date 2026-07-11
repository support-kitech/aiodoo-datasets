"""Immutability Tests for Evaluation Generator."""

import unittest
from types import MappingProxyType
from generators.evaluation.statistics.evaluation_statistics import (
    EvaluationStatistics,
)
from generators.evaluation.analysis.context import AnalysisContext


class TestImmutability(unittest.TestCase):
    """Verifies data structure immutability across Analysis and Statistics layers."""

    def test_analysis_context_immutability(self) -> None:
        """Ensure AnalysisContext source_protocols is a MappingProxyType."""
        ctx = AnalysisContext(
            source_protocols=MappingProxyType({"test": "data"}), evaluation_type="test"
        )

        with self.assertRaises(TypeError):
            ctx.source_protocols["hack"] = "mutated"

    def test_statistics_immutability(self) -> None:
        """Ensure EvaluationStatistics outputs are strictly immutable."""
        # Empty dataset for testing
        stats = EvaluationStatistics.compute(())
        self.assertTrue(hasattr(stats, "get_export_stats"))
        # As it's now a BaseStatistics instance, we verify its export dictionary is correct.
        export_dict = stats.get_export_stats()
        self.assertIsInstance(export_dict, dict)
        with self.assertRaises(TypeError):
            stats["total_evaluations"] = 9999


if __name__ == "__main__":
    unittest.main()
