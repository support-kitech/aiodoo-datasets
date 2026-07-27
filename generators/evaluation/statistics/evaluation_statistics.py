"""Evaluation Statistics for Evaluation Generator."""

from typing import Any, Tuple

from generators.common.statistics.base_statistics import BaseStatistics


class EvaluationStatistics(BaseStatistics):
    """Computes deterministic aggregates for Evaluation SFT / catalog exports."""

    def __init__(self) -> None:
        BaseStatistics.__init__(self)
        self.total_evaluations = 0
        self.total_judgments = 0
        self.total_catalogs = 0
        self.total_suites = 0
        self.total_cases = 0
        self.total_rules = 0
        self.total_references = 0
        self.total_expected_outputs = 0
        self.total_ground_truths = 0
        self.verdict_counts: dict[str, int] = {}

    def add_sample(self, record: Any, json_str: str) -> None:
        """Stream a single protocol record and update statistics."""
        self.total_samples += 1
        self.total_tokens += len(json_str) // 4

        if isinstance(record, dict):
            if record.get("verdict") is not None:
                self.total_judgments += 1
                verdict = str(record.get("verdict"))
                self.verdict_counts[verdict] = self.verdict_counts.get(verdict, 0) + 1
            catalog = record.get("catalog")
            if isinstance(catalog, dict):
                self.total_catalogs += 1
                suites = catalog.get("suites")
                if isinstance(suites, list):
                    self.total_suites += len(suites)
                    for suite in suites:
                        if isinstance(suite, dict):
                            cases = suite.get("cases")
                            if isinstance(cases, list):
                                self.total_cases += len(cases)
            return

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
            "total_judgments": self.total_judgments,
            "verdict_counts": dict(self.verdict_counts),
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
            stats.add_sample(record, "{}")
        return stats
