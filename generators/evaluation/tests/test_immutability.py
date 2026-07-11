"""Immutability Tests for Evaluation Generator."""

import unittest
from types import MappingProxyType
from aiodoo_datasets.generators.evaluation.statistics.evaluation_statistics import (
    EvaluationStatistics,
)
from aiodoo_datasets.generators.evaluation.analysis.context import AnalysisContext


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

        self.assertIsInstance(stats, MappingProxyType)
        with self.assertRaises(TypeError):
            stats["total_evaluations"] = 9999


if __name__ == "__main__":
    unittest.main()
