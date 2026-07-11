import unittest
from unittest.mock import patch
from aiodoo_datasets.generators.execution.registries.analyzer_registry import AnalyzerRegistry
from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext


class DummyAnalyzer1(BaseAnalyzer):
    PRIORITY = 10

    def analyze(self, context: AnalysisContext):
        pass


class DummyAnalyzer2(BaseAnalyzer):
    PRIORITY = 10

    def analyze(self, context: AnalysisContext):
        pass


class DummyAnalyzer3(BaseAnalyzer):
    # Missing PRIORITY
    def analyze(self, context: AnalysisContext):
        pass


class TestAnalyzerRegistry(unittest.TestCase):
    def test_ordering(self) -> None:
        analyzers = AnalyzerRegistry.get_analyzers()
        priorities = [a.PRIORITY for a in analyzers]

        # Verify strict ascending sort
        self.assertEqual(priorities, sorted(priorities))

    @patch(
        "aiodoo_datasets.generators.execution.registries.analyzer_registry._REGISTERED_ANALYZERS",
        (DummyAnalyzer1, DummyAnalyzer2),
    )
    def test_duplicate_priority_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate PRIORITY 10"):
            AnalyzerRegistry.get_analyzers()

    @patch(
        "aiodoo_datasets.generators.execution.registries.analyzer_registry._REGISTERED_ANALYZERS",
        (DummyAnalyzer3,),
    )
    def test_missing_priority_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "DummyAnalyzer3 missing PRIORITY"):
            AnalyzerRegistry.get_analyzers()


if __name__ == "__main__":
    unittest.main()
