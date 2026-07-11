"""Benchmark Validator for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.exceptions import EvaluationValidationError
from aiodoo_datasets.generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from aiodoo_datasets.generators.evaluation.domain.benchmark_suite import BenchmarkSuite


class BenchmarkValidator:
    """Validates BenchmarkCatalog and BenchmarkSuites."""

    @staticmethod
    def validate_catalog(catalog: BenchmarkCatalog) -> None:
        """Fail-fast validation."""
        if not catalog.catalog_id.startswith("CTLG-"):
            raise EvaluationValidationError(f"Invalid BenchmarkCatalog ID: {catalog.catalog_id}")

        if not catalog.suites:
            raise EvaluationValidationError(
                "BenchmarkCatalog must contain at least one BenchmarkSuite."
            )

        for suite in catalog.suites:
            BenchmarkValidator.validate_suite(suite)

    @staticmethod
    def validate_suite(suite: BenchmarkSuite) -> None:
        """Fail-fast validation."""
        if not suite.suite_id.startswith("SUITE-"):
            raise EvaluationValidationError(f"Invalid BenchmarkSuite ID: {suite.suite_id}")

        if not suite.cases:
            raise EvaluationValidationError(f"BenchmarkSuite {suite.suite_id} contains no cases.")
