"""Tests for ACT-103: real (non-stub) validation in ``evaluation.api.validate``.

Regression coverage for "Restore or remove datasets evaluation validate"
(`ecosystem-v2-certification/MASTER_ACTION_LIST.md`): the function
previously always returned ``True`` regardless of input. It must now
fail-closed: reject empty datasets, reject non-:class:`Evaluation` elements,
and delegate to the real domain validators (:class:`EvaluationValidator`,
:class:`DatasetValidator`), returning ``False`` on any violation.
"""

from __future__ import annotations

from dataclasses import replace

from generators.evaluation import api
from generators.evaluation.builders.benchmark_catalog_builder import (
    BenchmarkCatalogBuilder,
)
from generators.evaluation.builders.benchmark_suite_builder import (
    BenchmarkSuiteBuilder,
)
from generators.evaluation.builders.evaluation_builder import EvaluationBuilder
from generators.evaluation.builders.evaluation_case_builder import (
    EvaluationCaseBuilder,
)
from generators.evaluation.builders.expected_output_builder import (
    ExpectedOutputBuilder,
)
from generators.evaluation.builders.ground_truth_builder import GroundTruthBuilder
from generators.evaluation.builders.metadata_builder import MetadataBuilder
from generators.evaluation.domain.evaluation import Evaluation
from generators.evaluation.enums import (
    BenchmarkCategory,
    DifficultyLevel,
    EvaluationType,
)


def _build_valid_evaluation(source_identifier: str = "mod_a") -> Evaluation:
    """Builds a minimal, structurally valid Evaluation aggregate.

    Mirrors the Builder & Factory layer in
    ``generators/evaluation/pipeline/pipeline.py`` so the resulting object is
    representative of what the real pipeline produces, without needing to
    drive the full Analysis layer (parsers/extractors) with fake upstream
    protocol records.
    """
    eval_metadata = MetadataBuilder.build_evaluation_metadata(
        generator_version="1.0.0",
        protocol_version="1.0.0",
        schema_version="1.0.0",
        source_module=source_identifier,
        odoo_version="17.0",
        odoo_edition="CE",
        evaluation_type=EvaluationType.REPAIR,
        difficulty=DifficultyLevel.MEDIUM,
        complexity=1,
    )
    bench_metadata = MetadataBuilder.build_benchmark_metadata(
        suite_version="1.0.0",
        benchmark_version="1.0.0",
        benchmark_name="unit_test_benchmark",
        benchmark_category=BenchmarkCategory.CORE,
        benchmark_description="Unit test benchmark.",
        target_generator="aiodoo",
        supported_odoo_versions=("17.0",),
        supported_protocols=("repair",),
    )

    # These placeholder IDs only seed the deterministic hash-based IDs the
    # factories assign to the *real* suite/case/output/ground-truth objects
    # (see `EvaluationPipeline.run`'s "TEMP-*" placeholders); they must vary
    # per source_identifier so multiple Evaluations combined into one dataset
    # don't collide on case/output/ground-truth IDs.
    temp_case_seed = f"TEMP-0-{source_identifier}"
    expected_output = ExpectedOutputBuilder.build(
        case_id=temp_case_seed, expected_value="val", value_type="string", required_elements=()
    )
    ground_truth = GroundTruthBuilder.build(
        case_id=temp_case_seed, exact_match_required=False, keywords=()
    )
    case = EvaluationCaseBuilder.build(
        suite_id=f"SUITE-TMP-{source_identifier}",
        sequence_index=0,
        prompt="Eval prompt for 0",
        metadata=eval_metadata,
        expected_output=expected_output,
        ground_truth=ground_truth,
    )
    # Suite IDs are derived deterministically from (catalog_id, category), so
    # each source_identifier needs a distinct catalog_id to avoid collisions
    # when multiple Evaluations are combined into one dataset.
    catalog_id = f"CTLG-TMP-{source_identifier}"
    suite = BenchmarkSuiteBuilder.build(
        catalog_id=catalog_id,
        suite_category=BenchmarkCategory.CORE,
        suite_name=f"unit_test_benchmark Suite ({source_identifier})",
        cases=(case,),
    )
    catalog = BenchmarkCatalogBuilder.build(
        evaluation_id="EVALROOT-TMP",
        catalog_name="unit_test_benchmark",
        metadata=bench_metadata,
        suites=(suite,),
    )
    return EvaluationBuilder.build(
        generator_version="1.0.0",
        source_identifier=source_identifier,
        metadata=eval_metadata,
        catalog=catalog,
    )


class TestValidateFailsClosedOnMalformedInput:
    def test_empty_dataset_is_rejected(self) -> None:
        assert api.validate(()) is False

    def test_non_evaluation_element_is_rejected(self) -> None:
        assert api.validate(({"not": "an evaluation"},)) is False

    def test_mixed_valid_and_invalid_elements_is_rejected(self) -> None:
        valid = _build_valid_evaluation()
        assert api.validate((valid, "not an evaluation")) is False


class TestValidateAcceptsWellFormedDataset:
    def test_single_valid_evaluation_is_accepted(self) -> None:
        assert api.validate((_build_valid_evaluation(),)) is True

    def test_multiple_valid_evaluations_with_distinct_ids_are_accepted(self) -> None:
        dataset = (_build_valid_evaluation("mod_a"), _build_valid_evaluation("mod_b"))
        assert api.validate(dataset) is True


class TestValidateRejectsDomainViolations:
    def test_invalid_evaluation_root_id_is_rejected(self) -> None:
        evaluation = _build_valid_evaluation()
        broken = replace(evaluation, evaluation_id="NOT-A-VALID-ID")

        assert api.validate((broken,)) is False

    def test_duplicate_evaluation_ids_are_rejected(self) -> None:
        evaluation = _build_valid_evaluation()

        assert api.validate((evaluation, evaluation)) is False

    def test_catalog_with_no_suites_is_rejected(self) -> None:
        evaluation = _build_valid_evaluation()
        empty_catalog = replace(evaluation.catalog, suites=())
        broken = replace(evaluation, catalog=empty_catalog)

        assert api.validate((broken,)) is False
