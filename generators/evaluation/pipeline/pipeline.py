"""Pipeline for Evaluation Generator (SFT judgments + separate BenchmarkCatalog)."""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Any

from generators.common.export.writer import DatasetWriter
from generators.evaluation.builders.catalog_export import build_benchmark_catalog_record
from generators.evaluation.builders.judgment_builder import JudgmentBuilder, judgment_to_record
from generators.evaluation.pipeline.pipeline_context import PipelineContext
from generators.evaluation.pipeline.pipeline_result import PipelineResult
from generators.evaluation.policy import MIN_PRODUCTION_RECORDS, REQUIRED_SOURCE_TYPES
from generators.evaluation.statistics.evaluation_statistics import EvaluationStatistics


class EvaluationPipeline:
    """Orchestrates Evaluation capability SFT generation and catalog export."""

    REQUIRED_SOURCE_TYPES = frozenset(REQUIRED_SOURCE_TYPES)

    @staticmethod
    def run(context: PipelineContext) -> PipelineResult:
        """Build many judgment records; keep BenchmarkCatalog as a side artifact."""
        missing_sources = sorted(
            source_type
            for source_type in EvaluationPipeline.REQUIRED_SOURCE_TYPES
            if not context.source_protocols.get(source_type)
        )
        if missing_sources:
            raise RuntimeError(
                "Evaluation generation requires upstream artifacts for: "
                + ", ".join(missing_sources)
            )

        judgments = JudgmentBuilder.build_all(context.source_protocols)
        if len(judgments) < MIN_PRODUCTION_RECORDS:
            raise RuntimeError(
                "Evaluation production dataset rejected: "
                f"only {len(judgments)} judgment(s); "
                f"minimum is {MIN_PRODUCTION_RECORDS} "
                "(single BenchmarkCatalog placeholder grain forbidden)"
            )

        records = tuple(judgment_to_record(case) for case in judgments)
        catalog_record = build_benchmark_catalog_record(
            judgments,
            benchmark_name=context.benchmark_name,
            benchmark_category=context.benchmark_category,
            benchmark_description=context.benchmark_description,
            target_generator=context.target_generator,
        )

        stats = MappingProxyType(
            {
                "judgments": len(records),
                "by_verdict": _count_verdicts(records),
                "by_capability": _count_capabilities(records),
                "catalog_suites": len(catalog_record["catalog"]["suites"]),
                "catalog_cases": catalog_record["metadata"]["case_count"],
            }
        )

        return PipelineResult(
            dataset=records,
            statistics=stats,
            validation_passed=True,
            protocol_context=getattr(context, "protocol_context", None),
            catalog=catalog_record,
        )

    @staticmethod
    def export(result: PipelineResult, output_dir: str) -> PipelineResult:
        """Export SFT judgments and a separate BenchmarkCatalog artifact."""
        if not result.validation_passed or not result.dataset:
            raise RuntimeError("Evaluation generation did not produce an exportable dataset.")

        output_path = Path(output_dir)
        sft_stats = EvaluationStatistics()
        sft_writer = DatasetWriter(
            output_dir=output_path,
            stats=sft_stats,
            filename="evaluation_dataset.jsonl",
            dataset_name="evaluation",
        )
        for record in result.dataset:
            sft_writer.write_record(record)
        sft_writer.export_statistics(filename="evaluation_statistics.json")
        sft_writer.export_manifest(filename="evaluation_manifest.json")

        catalog = result.catalog
        if catalog is not None:
            catalog_stats = EvaluationStatistics()
            catalog_writer = DatasetWriter(
                output_dir=output_path,
                stats=catalog_stats,
                filename="evaluation_benchmark_catalog.jsonl",
                dataset_name="benchmark_catalog",
            )
            catalog_writer.write_record(catalog)
            catalog_writer.export_statistics(
                filename="evaluation_benchmark_catalog_statistics.json"
            )
            catalog_writer.export_manifest(filename="evaluation_benchmark_catalog_manifest.json")

        export_metadata = MappingProxyType(
            {
                "output_dir": output_dir,
                "exported_sft_records": len(result.dataset),
                "exported_catalog": catalog is not None,
            }
        )
        return PipelineResult(
            dataset=result.dataset,
            statistics=result.statistics,
            validation_passed=result.validation_passed,
            export_metadata=export_metadata,
            protocol_context=result.protocol_context,
            catalog=result.catalog,
        )


def _count_verdicts(records: tuple[dict[str, Any], ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        key = str(record.get("verdict", "unknown"))
        counts[key] = counts.get(key, 0) + 1
    return counts


def _count_capabilities(records: tuple[dict[str, Any], ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        key = str(record.get("capability_under_test", "unknown"))
        counts[key] = counts.get(key, 0) + 1
    return counts
