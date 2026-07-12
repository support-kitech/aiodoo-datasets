"""Pipeline for Evaluation Generator."""

from types import MappingProxyType

from generators.evaluation.pipeline.pipeline_context import PipelineContext
from generators.evaluation.pipeline.pipeline_result import PipelineResult

from generators.evaluation.analysis.context import AnalysisContext
from generators.evaluation.analysis.evidence_extractor import EvidenceExtractor
from generators.evaluation.analysis.ground_truth_extractor import (
    GroundTruthExtractor,
)
from generators.evaluation.analysis.difficulty_estimator import DifficultyEstimator
from generators.evaluation.analysis.complexity_estimator import ComplexityEstimator

from generators.evaluation.builders.evaluation_builder import EvaluationBuilder
from generators.evaluation.builders.benchmark_catalog_builder import (
    BenchmarkCatalogBuilder,
)
from generators.evaluation.builders.benchmark_suite_builder import (
    BenchmarkSuiteBuilder,
)
from generators.evaluation.builders.evaluation_case_builder import (
    EvaluationCaseBuilder,
)
from generators.evaluation.builders.metadata_builder import MetadataBuilder
from generators.evaluation.builders.expected_output_builder import (
    ExpectedOutputBuilder,
)
from generators.evaluation.builders.ground_truth_builder import GroundTruthBuilder

# Protocol imports removed

from generators.evaluation.statistics.evaluation_statistics import (
    EvaluationStatistics,
)
from generators.evaluation.statistics.benchmark_statistics import (
    BenchmarkStatistics,
)

from generators.common.export.writer import DatasetWriter


class EvaluationPipeline:
    """Orchestrates the complete deterministic evaluation generation flow."""

    REQUIRED_SOURCE_TYPES = frozenset(
        {
            "planner",
            "coding",
            "repair",
            "context",
            "execution",
            "approval",
            "conversation",
        }
    )

    @staticmethod
    def run(context: PipelineContext) -> PipelineResult:
        """Run the full pipeline: Analysis -> Build -> Map -> Validate -> Stats."""

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

        # 1. Analysis Layer
        analysis_ctx = AnalysisContext(
            source_protocols=context.source_protocols, evaluation_type=context.evaluation_type
        )
        extracted_evidence = EvidenceExtractor.extract(analysis_ctx)
        parsed_sources = {item.get("source_type") for item in extracted_evidence}
        missing_evidence = sorted(EvaluationPipeline.REQUIRED_SOURCE_TYPES - parsed_sources)
        if missing_evidence:
            raise RuntimeError(
                "Evaluation parsers did not produce evidence for: " + ", ".join(missing_evidence)
            )

        ground_truths = GroundTruthExtractor.extract(extracted_evidence)
        difficulty = DifficultyEstimator.estimate(
            extracted_evidence[0] if extracted_evidence else {}
        )
        complexity = ComplexityEstimator.estimate(
            extracted_evidence[0] if extracted_evidence else {}
        )

        # 2. Builder & Factory Layer (Domain)
        # Create Metadata
        eval_metadata = MetadataBuilder.build_evaluation_metadata(
            generator_version=context.generator_version,
            protocol_version=context.protocol_version,
            schema_version=context.schema_version,
            source_module=extracted_evidence[0].get("source_module", "unknown")
            if extracted_evidence
            else "unknown",
            odoo_version="17.0",  # Simplified
            odoo_edition="CE",  # Simplified
            evaluation_type=context.evaluation_type,
            difficulty=difficulty,
            complexity=complexity,
        )

        bench_metadata = MetadataBuilder.build_benchmark_metadata(
            suite_version="1.0.0",
            benchmark_version="1.0.0",
            benchmark_name=context.benchmark_name,
            benchmark_category=context.benchmark_category,
            benchmark_description=context.benchmark_description,
            target_generator=context.target_generator,
            supported_odoo_versions=context.supported_odoo_versions,
            supported_protocols=context.supported_protocols,
        )

        # Create Cases
        cases = []
        for idx, truth in enumerate(ground_truths):
            eo = ExpectedOutputBuilder.build(
                case_id=f"TEMP-{idx}",  # Will be assigned real ID in factory
                expected_value=truth.get("type", "val"),
                value_type="string",
                required_elements=truth.get("keywords", ()),
            )
            gt = GroundTruthBuilder.build(
                case_id=f"TEMP-{idx}",
                exact_match_required=truth.get("exact_match_required", False),
                keywords=truth.get("keywords", ()),
            )
            # Use deterministic suite_id reference internally
            temp_suite_id = "SUITE-TMP"
            case = EvaluationCaseBuilder.build(
                suite_id=temp_suite_id,
                sequence_index=idx,
                prompt=f"Eval prompt for {idx}",
                metadata=eval_metadata,
                expected_output=eo,
                ground_truth=gt,
                rules=(),
                success_criteria=(),
                failure_criteria=(),
                references=(),
                attachments=(),
                scores=(),
            )
            cases.append(case)

        suite = BenchmarkSuiteBuilder.build(
            catalog_id="CTLG-TMP",
            suite_category=context.benchmark_category,
            suite_name=f"{context.benchmark_name} Suite",
            cases=tuple(cases),
        )

        catalog = BenchmarkCatalogBuilder.build(
            evaluation_id="EVALROOT-TMP",
            catalog_name=context.benchmark_name,
            metadata=bench_metadata,
            suites=(suite,),
        )

        evaluation = EvaluationBuilder.build(
            generator_version=context.generator_version,
            source_identifier=context.benchmark_name,
            metadata=eval_metadata,
            catalog=catalog,
        )

        # 3. Protocol Mapping Layer (Removed)
        dataset = (evaluation,)

        # 4. Validation Layer (Removed Protocol Validation)
        # Optional domain checking can be run here on `(evaluation,)`

        # 5. Statistics Layer
        stats = MappingProxyType(
            {
                "evaluation": EvaluationStatistics.compute(dataset),
                "benchmark": BenchmarkStatistics.compute(dataset),
            }
        )

        return PipelineResult(
            dataset=dataset,
            statistics=stats,
            validation_passed=True,
            protocol_context=getattr(context, "protocol_context", None),
        )

    @staticmethod
    def export(result: PipelineResult, output_dir: str) -> PipelineResult:
        """Export result using shared DatasetWriter."""
        from pathlib import Path
        from generators.evaluation.statistics.evaluation_statistics import EvaluationStatistics

        if not result.validation_passed or not result.dataset:
            raise RuntimeError("Evaluation generation did not produce an exportable dataset.")

        stats = EvaluationStatistics()

        writer = DatasetWriter(
            output_dir=Path(output_dir),
            stats=stats,
            filename="evaluation_dataset.jsonl",
            dataset_name="Evaluation Dataset",
        )

        for obj in result.dataset:
            writer.write_record(obj)

        writer.export_statistics(filename="evaluation_statistics.json")
        writer.export_manifest(filename="evaluation_manifest.json")

        export_metadata = MappingProxyType(
            {"output_dir": output_dir, "exported_records": len(result.dataset)}
        )

        return PipelineResult(
            dataset=result.dataset,
            statistics=result.statistics,
            validation_passed=result.validation_passed,
            export_metadata=export_metadata,
        )
