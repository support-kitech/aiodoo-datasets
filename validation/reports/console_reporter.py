"""Console reporter for human-readable terminal output."""

import logging
from pathlib import Path

from validation.domain.enums import ValidationSeverity
from validation.domain.results import ValidationReport
from validation.reports.base import BaseReporter

logger = logging.getLogger(__name__)

SEVERITY_SYMBOLS = {
    ValidationSeverity.FATAL: "💀",
    ValidationSeverity.ERROR: "❌",
    ValidationSeverity.WARNING: "⚠️",
    ValidationSeverity.INFO: "ℹ️",
}


class ConsoleReporter(BaseReporter):
    """Prints a formatted validation report to the console."""

    def report(self, report: ValidationReport, output_dir: Path) -> None:
        """Print the validation report to stdout via logging."""
        summary = report.summary

        logger.info("=" * 60)
        logger.info("VALIDATION REPORT")
        logger.info("=" * 60)
        logger.info("Framework Version: %s", report.framework_version)
        logger.info("Timestamp: %s", report.timestamp)
        logger.info("")

        # Per-dataset results
        for result in report.results:
            status_icon = "✅" if result.status.value == "passed" else "❌"
            logger.info(
                "%s %s — %d records, %d issues",
                status_icon,
                result.dataset_name,
                result.records_validated,
                len(result.issues),
            )

            # Group issues by severity
            for severity in ValidationSeverity:
                severity_issues = [i for i in result.issues if i.severity == severity]
                for issue in severity_issues[:5]:  # Cap display per severity
                    symbol = SEVERITY_SYMBOLS.get(severity, "?")
                    line_info = (
                        f" (line {issue.record_index})" if issue.record_index is not None else ""
                    )
                    logger.info(
                        "  %s [%s] %s%s",
                        symbol,
                        issue.rule_id,
                        issue.message,
                        line_info,
                    )
                if len(severity_issues) > 5:
                    logger.info(
                        "  ... and %d more %s issues",
                        len(severity_issues) - 5,
                        severity.value,
                    )

        # Summary
        logger.info("")
        logger.info("-" * 60)
        result_icon = "✅ PASSED" if summary.passed else "❌ FAILED"
        logger.info("Result: %s", result_icon)
        logger.info(
            "Datasets: %d | Records: %d | Issues: %d",
            summary.total_datasets,
            summary.total_records,
            summary.total_issues,
        )
        logger.info(
            "Fatal: %d | Error: %d | Warning: %d | Info: %d",
            summary.fatal_count,
            summary.error_count,
            summary.warning_count,
            summary.info_count,
        )
        logger.info("Health Score: %.1f / 100.0", summary.health_score)
        logger.info("Duration: %.1fms", summary.duration_ms)

        # Per-category breakdown
        if summary.per_category_counts:
            logger.info("")
            logger.info("By Category:")
            for cat, count in sorted(summary.per_category_counts.items()):
                logger.info("  %-16s %d issues", cat, count)

        logger.info("=" * 60)
