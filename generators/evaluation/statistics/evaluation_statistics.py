"""Evaluation Statistics for Evaluation Generator."""

from typing import Tuple, Any

# removed EvaluationProtocol import
from generators.common.statistics.base_statistics import BaseStatistics


class EvaluationStatistics(BaseStatistics):
    """Computes deterministic aggregates for the entire evaluation dataset."""

    def __init__(self) -> None:
        BaseStatistics.__init__(self)
        self.total_evaluations = 0
        self.total_catalogs = 0
        self.total_suites = 0
        self.total_cases = 0
        self.total_rules = 0
        self.total_references = 0
        self.total_expected_outputs = 0
        self.total_ground_truths = 0

    def add_sample(self, record: Any, json_str: str) -> None:
        """Stream a single protocol record and update statistics."""
        # For evaluation, we only perform minimal base updates if needed,
        # since Evaluation uses a domain-specific model.
        # Ensure base counters still increment.
        self.total_samples += 1
        self.total_tokens += len(json_str) // 4

        # Now process the specific Evaluation payload
        if not hasattr(record, "catalog"):
            return

        self.total_evaluations += 1
        if record.catalog:
            self.total_catalogs += 1
            for suite in record.catalog.suites:
                self.total_suites += 1
                for case in suite.cases:
                    self.total_cases += 1
                    self.total_rules += len(case.rules)
                    self.total_references += len(case.references)

                    if case.expected_output:
                        self.total_expected_outputs += 1
                    if case.ground_truth:
                        self.total_ground_truths += 1

    def get_export_stats(self) -> dict[str, Any]:
        """Export domain-specific aggregates."""
        return {
            "total_evaluations": self.total_evaluations,
            "total_catalogs": self.total_catalogs,
            "total_suites": self.total_suites,
            "total_cases": self.total_cases,
            "total_rules": self.total_rules,
            "total_references": self.total_references,
            "total_expected_outputs": self.total_expected_outputs,
            "total_ground_truths": self.total_ground_truths,
        }

    @staticmethod
    def compute(dataset: Tuple[Any, ...]) -> "EvaluationStatistics":
        """Backwards compatibility for compute() pattern."""
        stats = EvaluationStatistics()
        for record in dataset:
            stats.add_sample(record, "{}")  # Dummy string for json size
        return stats
