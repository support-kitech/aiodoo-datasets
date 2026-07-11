"""Main orchestration pipeline for the Validation Framework."""

import logging
import time
from types import MappingProxyType

from validation.domain.results import ValidationResult
from validation.builders.report_builder import ReportBuilder
from validation.pipeline.pipeline_context import PipelineContext
from validation.pipeline.pipeline_result import PipelineResult
from validation.pipeline.pipeline_statistics import PipelineStatistics
from validation.validators.dataset_validator import DatasetValidator
from validation.validators.cross_dataset_validator import CrossDatasetValidator
from validation.validators.manifest_validator import ManifestValidator

logger = logging.getLogger(__name__)


class ValidationPipeline:
    """
    Coordinates the full validation lifecycle.

    Flow:
    1. Schema resolution per dataset
    2. Per-dataset validation (with resolved schema)
    3. Manifest validation
    4. Cross-dataset validation
    5. Report aggregation
    """

    def execute(self, context: PipelineContext) -> PipelineResult:
        """Execute the full validation pipeline."""
        start = time.perf_counter()

        try:
            results: list[ValidationResult] = []
            per_dataset_durations: dict[str, float] = {}

            val_context = context.validation_context
            registry = context.registry
            schema_registry = context.schema_registry
            options = context.options

            # 1. Per-dataset validation with schema resolution
            if options.validate_datasets:
                for jsonl_path in val_context.dataset_files:
                    dataset_name = jsonl_path.name
                    rules = registry.get_rules_for_dataset(dataset_name)

                    # Resolve schema for this dataset
                    schema = schema_registry.resolve_from_filename(dataset_name)
                    schema_label = f" → {schema.schema_id}" if schema else " → fallback"
                    logger.info(
                        "Validating %s%s (%d rules)...",
                        dataset_name,
                        schema_label,
                        len(rules),
                    )

                    result = DatasetValidator.validate(
                        jsonl_path=jsonl_path,
                        rules=rules,
                        context=val_context,
                        max_issues=options.max_issues_per_dataset,
                        schema=schema,
                    )
                    results.append(result)
                    per_dataset_durations[dataset_name] = result.duration_ms

                    # Fail fast on FATAL
                    if options.fail_fast and result.fatal_count > 0:
                        logger.error("Fail-fast triggered by FATAL issue in %s", dataset_name)
                        break

            # 2. Manifest validation
            if options.validate_manifests:
                logger.info("Validating manifests...")
                manifest_result = ManifestValidator.validate(val_context)
                results.append(manifest_result)

            # 3. Cross-dataset validation
            if options.validate_cross_dataset and len(val_context.dataset_files) > 1:
                logger.info("Running cross-dataset validation...")
                cross_result = CrossDatasetValidator.validate(val_context)
                results.append(cross_result)

            # 4. Build report
            report = ReportBuilder.build(tuple(results), options)

            total_ms = (time.perf_counter() - start) * 1000
            statistics = PipelineStatistics(
                datasets_validated=len(val_context.dataset_files),
                records_validated=sum(r.records_validated for r in results),
                rules_executed=sum(
                    len(registry.get_rules_for_dataset(f.name))
                    for f in val_context.dataset_files
                ),
                total_duration_ms=total_ms,
                per_dataset_durations=MappingProxyType(per_dataset_durations),
            )

            return PipelineResult(
                success=report.summary.passed,
                report=report,
                statistics=statistics,
            )

        except Exception as e:
            total_ms = (time.perf_counter() - start) * 1000
            logger.error("Validation pipeline error: %s", e)
            report = ReportBuilder.build(())
            return PipelineResult(
                success=False,
                report=report,
                statistics=PipelineStatistics(total_duration_ms=total_ms),
                error_message=str(e),
            )
