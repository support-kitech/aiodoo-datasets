"""Pipeline orchestrator for the Approval Generator.

Emits one JSONL record per upstream subject (planner/coding/repair/execution),
never a corpus-wide single Review.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from generators.approval.analysis.subject import SubjectPartitioner
from generators.approval.builders.review_builder import SubjectReviewBuilder
from generators.approval.exceptions import ApprovalPipelineError
from generators.approval.pipeline_context import PipelineContext
from generators.approval.pipeline_result import PipelineResult
from generators.approval.policy import MIN_PRODUCTION_RECORDS
from generators.approval.statistics.approval_statistics import ApprovalStatistics
from generators.approval.validation.approval_validator import ApprovalValidator
from generators.common.export.writer import DatasetWriter
from generators.common.statistics.base_statistics import BaseStatistics


class ApprovalExportStatistics(BaseStatistics):  # type: ignore[misc]
    """Adapter for BaseStatistics to use in DatasetWriter."""

    def __init__(self, stats_dict: dict[str, Any]) -> None:
        BaseStatistics.__init__(self)
        self.stats_dict = stats_dict

    def add_sample(self, record: Any, json_str: str) -> None:  # type: ignore[no-untyped-def]
        self._add_base_sample(record, json_str)

    def get_export_stats(self) -> dict[str, Any]:  # type: ignore[no-untyped-def]
        merged = dict(self.stats_dict)
        merged.update(
            {
                "total_samples": self.total_samples,
                "total_modules": self.total_modules,
                "duplicate_count": self.duplicate_count,
                "validation_failures": self.validation_failures,
            }
        )
        return merged


class ApprovalPipeline:
    """Orchestrates subject-partitioned Approval generation."""

    @staticmethod
    def generate(context: PipelineContext) -> PipelineResult:
        """Execute the pipeline: partition → decide per subject → write N records."""
        diagnostics: list[str] = []

        try:
            required_inputs = ("planner_data", "coding_data", "repair_data", "execution_data")
            missing_inputs = tuple(
                name for name in required_inputs if not context.input_protocols.get(name)
            )
            if missing_inputs:
                return PipelineResult(
                    success=False,
                    diagnostics=tuple(
                        f"Missing required upstream artifact: {name}" for name in missing_inputs
                    ),
                )

            subjects = SubjectPartitioner.extract(context.input_protocols)
            if not subjects:
                return PipelineResult(
                    success=False,
                    diagnostics=("No approval subjects extracted from upstream datasets",),
                )

            reviews = []
            seen_record_ids: set[str] = set()
            for subject in subjects:
                if subject.record_id in seen_record_ids:
                    diagnostics.append(f"Skipped duplicate subject record_id={subject.record_id}")
                    continue
                seen_record_ids.add(subject.record_id)

                review = SubjectReviewBuilder.build(
                    subject,
                    base_metadata=context.metadata,
                    rule_set=context.rule_set,
                    parser_registry_cls=context.parser_registry_cls,
                )
                ApprovalValidator.validate_all(review, review)
                reviews.append(review)

            reviews.sort(key=lambda r: r.record_id or r.review_id)

            if len(reviews) < MIN_PRODUCTION_RECORDS:
                return PipelineResult(
                    success=False,
                    diagnostics=(
                        "Approval production dataset rejected: "
                        f"only {len(reviews)} record(s); "
                        f"minimum is {MIN_PRODUCTION_RECORDS} (placeholder grain forbidden)",
                    ),
                )

            statistics = ApprovalStatistics.compile_many(reviews, context.rule_set)
            export_stats = ApprovalExportStatistics(dict(statistics))
            output_path = Path(context.config.output_dir)
            writer = DatasetWriter(
                output_dir=output_path,
                stats=export_stats,
                filename="approval_dataset.jsonl",
                dataset_name="approval",
            )

            for review in reviews:
                writer.write_record(review)

            writer.export_manifest("approval_manifest.json")
            writer.export_statistics("approval_statistics.json")

            exported_files = (
                str(output_path / "approval_dataset.jsonl"),
                str(output_path / "approval_manifest.json"),
                str(output_path / "approval_statistics.json"),
            )

            return PipelineResult(
                success=True,
                approval_protocol=tuple(reviews),
                statistics=statistics,
                diagnostics=tuple(diagnostics),
                exported_files=exported_files,
            )

        except Exception as e:
            raise ApprovalPipelineError(f"Pipeline execution failed: {str(e)}") from e
