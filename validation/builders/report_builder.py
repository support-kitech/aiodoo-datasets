"""Builds ValidationReport from individual ValidationResults."""

from collections import Counter
from datetime import datetime, timezone

from validation.constants.framework import VALIDATION_FRAMEWORK_VERSION
from validation.domain.enums import ValidationSeverity
from validation.domain.results import ValidationResult, ValidationSummary, ValidationReport
from validation.pipeline.pipeline_options import ValidationOptions


class ReportBuilder:
    """Aggregates ValidationResults into a ValidationReport."""

    @staticmethod
    def build(
        results: tuple[ValidationResult, ...],
        options: ValidationOptions | None = None,
    ) -> ValidationReport:
        """
        Build an immutable ValidationReport from individual results.

        Args:
            results: Tuple of per-dataset ValidationResults.
            options: The options used for this validation run.

        Returns:
            An immutable ValidationReport.
        """
        from types import MappingProxyType

        total_records = sum(r.records_validated for r in results)
        all_issues = []
        for r in results:
            all_issues.extend(r.issues)

        fatal = sum(1 for i in all_issues if i.severity == ValidationSeverity.FATAL)
        error = sum(1 for i in all_issues if i.severity == ValidationSeverity.ERROR)
        warning = sum(1 for i in all_issues if i.severity == ValidationSeverity.WARNING)
        info = sum(1 for i in all_issues if i.severity == ValidationSeverity.INFO)
        total_duration = sum(r.duration_ms for r in results)

        passed = fatal == 0 and error == 0

        # Per-category issue counts
        category_counts: Counter[str] = Counter()
        for issue in all_issues:
            category_counts[issue.category.value] += 1

        # Per-generator (dataset) issue counts
        generator_counts: Counter[str] = Counter()
        for result in results:
            if result.issues:
                generator_counts[result.dataset_name] = len(result.issues)

        # Health score: 100 = perfect, penalize by severity
        if total_records > 0:
            penalty = (fatal * 10 + error * 5 + warning * 1) / total_records
            health_score = max(0.0, min(100.0, 100.0 - penalty * 100.0))
        else:
            health_score = 100.0 if not all_issues else 0.0

        summary = ValidationSummary(
            total_datasets=len(results),
            total_records=total_records,
            total_issues=len(all_issues),
            fatal_count=fatal,
            error_count=error,
            warning_count=warning,
            info_count=info,
            passed=passed,
            duration_ms=total_duration,
            per_category_counts=MappingProxyType(dict(category_counts)),
            per_generator_counts=MappingProxyType(dict(generator_counts)),
            health_score=round(health_score, 1),
        )

        options_dict: dict = {}
        if options is not None:
            options_dict = {
                "fail_fast": options.fail_fast,
                "parallel": options.parallel,
                "workers": options.workers,
                "report_format": options.report_format.value,
            }

        return ValidationReport(
            results=results,
            summary=summary,
            framework_version=VALIDATION_FRAMEWORK_VERSION,
            timestamp=datetime.now(timezone.utc).isoformat(),
            options=MappingProxyType(options_dict),
        )
