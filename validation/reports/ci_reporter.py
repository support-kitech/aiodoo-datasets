"""CI reporter for GitHub Actions annotations."""

import sys
from pathlib import Path

from validation.domain.enums import ValidationSeverity
from validation.domain.results import ValidationReport
from validation.reports.base import BaseReporter


class CIReporter(BaseReporter):
    """Outputs GitHub Actions-compatible annotations."""

    def report(self, report: ValidationReport, output_dir: Path) -> None:
        """Write GitHub Actions annotations to stdout."""
        for result in report.results:
            for issue in result.issues:
                level = self._gh_level(issue.severity)
                line = issue.record_index if issue.record_index is not None else 1
                print(
                    f"::{level} file={result.dataset_name},line={line}::"
                    f"[{issue.rule_id}] {issue.message}",
                    file=sys.stdout,
                )

        summary = report.summary
        if summary.passed:
            print("::notice::Validation PASSED", file=sys.stdout)
        else:
            print(
                f"::error::Validation FAILED: {summary.fatal_count} fatal, "
                f"{summary.error_count} errors, {summary.warning_count} warnings",
                file=sys.stdout,
            )

    @staticmethod
    def _gh_level(severity: ValidationSeverity) -> str:
        if severity in (ValidationSeverity.FATAL, ValidationSeverity.ERROR):
            return "error"
        if severity == ValidationSeverity.WARNING:
            return "warning"
        return "notice"
