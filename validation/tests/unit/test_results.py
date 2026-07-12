"""Unit tests for validation domain result models."""

import unittest

from validation.domain.enums import ValidationSeverity, ValidationStatus, ValidationCategory
from validation.domain.models import ValidationIssue
from validation.domain.results import ValidationResult, ValidationSummary, ValidationReport


class TestValidationIssue(unittest.TestCase):
    def test_immutable(self) -> None:
        issue = ValidationIssue(
            rule_id="SCH-001",
            severity=ValidationSeverity.FATAL,
            category=ValidationCategory.SCHEMA,
            message="Missing field",
            dataset_name="test.jsonl",
        )
        with self.assertRaises(AttributeError):
            issue.message = "changed"  # type: ignore[misc]

    def test_fields(self) -> None:
        issue = ValidationIssue(
            rule_id="INT-001",
            severity=ValidationSeverity.ERROR,
            category=ValidationCategory.INTEGRITY,
            message="Bad hash",
            dataset_name="test.jsonl",
            record_index=42,
            field_path="metadata.protocol_hash",
        )
        self.assertEqual(issue.rule_id, "INT-001")
        self.assertEqual(issue.record_index, 42)
        self.assertEqual(issue.field_path, "metadata.protocol_hash")


class TestValidationResult(unittest.TestCase):
    def test_success(self) -> None:
        r = ValidationResult.success(dataset_name="test.jsonl", records_validated=100)
        self.assertEqual(r.status, ValidationStatus.PASSED)
        self.assertEqual(r.issues, ())
        self.assertEqual(r.records_validated, 100)

    def test_failure(self) -> None:
        issue = ValidationIssue(
            rule_id="X",
            severity=ValidationSeverity.FATAL,
            category=ValidationCategory.SCHEMA,
            message="fail",
            dataset_name="t",
        )
        r = ValidationResult.failure(issue, dataset_name="t")
        self.assertEqual(r.status, ValidationStatus.FAILED)
        self.assertEqual(len(r.issues), 1)

    def test_merge(self) -> None:
        ok = ValidationResult.success(records_validated=10)
        issue = ValidationIssue(
            rule_id="X",
            severity=ValidationSeverity.ERROR,
            category=ValidationCategory.SCHEMA,
            message="m",
            dataset_name="d",
        )
        bad = ValidationResult.failure(issue, records_validated=5)
        merged = ok.merge(bad)
        self.assertEqual(merged.status, ValidationStatus.FAILED)
        self.assertEqual(merged.records_validated, 15)
        self.assertEqual(len(merged.issues), 1)

    def test_severity_counts(self) -> None:
        issues = (
            ValidationIssue(
                rule_id="A",
                severity=ValidationSeverity.FATAL,
                category=ValidationCategory.SCHEMA,
                message="",
                dataset_name="",
            ),
            ValidationIssue(
                rule_id="B",
                severity=ValidationSeverity.ERROR,
                category=ValidationCategory.SCHEMA,
                message="",
                dataset_name="",
            ),
            ValidationIssue(
                rule_id="C",
                severity=ValidationSeverity.WARNING,
                category=ValidationCategory.SCHEMA,
                message="",
                dataset_name="",
            ),
        )
        r = ValidationResult(status=ValidationStatus.FAILED, issues=issues)
        self.assertEqual(r.fatal_count, 1)
        self.assertEqual(r.error_count, 1)
        self.assertEqual(r.warning_count, 1)

    def test_immutable(self) -> None:
        r = ValidationResult.success()
        with self.assertRaises(AttributeError):
            r.status = ValidationStatus.FAILED  # type: ignore[misc]


class TestValidationSummary(unittest.TestCase):
    def test_defaults(self) -> None:
        s = ValidationSummary()
        self.assertTrue(s.passed)
        self.assertEqual(s.total_issues, 0)

    def test_immutable(self) -> None:
        s = ValidationSummary()
        with self.assertRaises(AttributeError):
            s.passed = False  # type: ignore[misc]


class TestValidationReport(unittest.TestCase):
    def test_defaults(self) -> None:
        r = ValidationReport()
        self.assertEqual(r.results, ())
        self.assertEqual(r.framework_version, "")


if __name__ == "__main__":
    unittest.main()
