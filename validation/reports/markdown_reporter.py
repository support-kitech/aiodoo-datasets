"""Markdown reporter for formatted reports."""

from pathlib import Path

from validation.domain.results import ValidationReport
from validation.reports.base import BaseReporter


class MarkdownReporter(BaseReporter):
    """Writes a VALIDATION_REPORT.md to the output directory."""

    def report(self, report: ValidationReport, output_dir: Path) -> None:
        """Write VALIDATION_REPORT.md."""
        lines: list[str] = []
        summary = report.summary

        lines.append("# Validation Report\n")
        lines.append(f"**Framework Version:** {report.framework_version}  ")
        lines.append(f"**Timestamp:** {report.timestamp}  ")
        lines.append(f"**Status:** {'✅ PASSED' if summary.passed else '❌ FAILED'}\n")

        # Summary table
        lines.append("## Summary\n")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Datasets | {summary.total_datasets} |")
        lines.append(f"| Records | {summary.total_records} |")
        lines.append(f"| Total Issues | {summary.total_issues} |")
        lines.append(f"| Fatal | {summary.fatal_count} |")
        lines.append(f"| Error | {summary.error_count} |")
        lines.append(f"| Warning | {summary.warning_count} |")
        lines.append(f"| Duration | {summary.duration_ms:.1f}ms |")
        lines.append("")

        # Per-dataset details
        if report.results:
            lines.append("## Datasets\n")
            for result in report.results:
                status = "✅" if result.status.value == "passed" else "❌"
                lines.append(f"### {status} {result.dataset_name}\n")
                lines.append(f"Records: {result.records_validated} | Issues: {len(result.issues)}\n")

                if result.issues:
                    lines.append("| Severity | Rule | Message |")
                    lines.append("|----------|------|---------|")
                    for issue in result.issues[:20]:
                        lines.append(f"| {issue.severity.value} | {issue.rule_id} | {issue.message} |")
                    if len(result.issues) > 20:
                        lines.append(f"\n*...and {len(result.issues) - 20} more issues*\n")
                    lines.append("")

        report_path = output_dir / "VALIDATION_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
