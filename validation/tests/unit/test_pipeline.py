"""Unit tests for the validation pipeline options and stages."""

import unittest

from validation.pipeline.pipeline_options import ValidationOptions
from validation.pipeline.pipeline_result import PipelineResult
from validation.pipeline.pipeline_statistics import PipelineStatistics
from validation.domain.enums import ReportFormat
from validation.domain.results import ValidationReport, ValidationSummary


class TestValidationOptions(unittest.TestCase):
    def test_defaults(self) -> None:
        opts = ValidationOptions()
        self.assertFalse(opts.fail_fast)
        self.assertTrue(opts.parallel)
        self.assertEqual(opts.workers, 4)
        self.assertTrue(opts.validate_schemas)
        self.assertTrue(opts.validate_datasets)
        self.assertTrue(opts.validate_manifests)
        self.assertTrue(opts.validate_cross_dataset)

    def test_immutable(self) -> None:
        opts = ValidationOptions()
        with self.assertRaises(AttributeError):
            opts.fail_fast = True  # type: ignore[misc]

    def test_custom_options(self) -> None:
        opts = ValidationOptions(
            fail_fast=True,
            parallel=False,
            workers=8,
            report_format=ReportFormat.JSON,
            validate_manifests=False,
        )
        self.assertTrue(opts.fail_fast)
        self.assertFalse(opts.parallel)
        self.assertEqual(opts.workers, 8)
        self.assertFalse(opts.validate_manifests)


class TestPipelineResult(unittest.TestCase):
    def test_immutable(self) -> None:
        result = PipelineResult(
            success=True,
            report=ValidationReport(),
            statistics=PipelineStatistics(),
        )
        with self.assertRaises(AttributeError):
            result.success = False  # type: ignore[misc]


class TestPipelineStatistics(unittest.TestCase):
    def test_defaults(self) -> None:
        stats = PipelineStatistics()
        self.assertEqual(stats.datasets_validated, 0)
        self.assertEqual(stats.records_validated, 0)
        self.assertEqual(stats.total_duration_ms, 0.0)


class TestValidationSummary(unittest.TestCase):
    def test_health_score(self) -> None:
        summary = ValidationSummary(
            total_records=100,
            total_issues=5,
            health_score=95.0,
            passed=True,
        )
        self.assertEqual(summary.health_score, 95.0)

    def test_per_category_counts(self) -> None:
        from types import MappingProxyType

        summary = ValidationSummary(
            per_category_counts=MappingProxyType({"schema": 3, "integrity": 2}),
        )
        self.assertEqual(summary.per_category_counts["schema"], 3)
        self.assertEqual(summary.per_category_counts["integrity"], 2)


if __name__ == "__main__":
    unittest.main()
