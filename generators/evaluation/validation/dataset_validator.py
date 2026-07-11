"""Dataset Validator for Evaluation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.evaluation.exceptions import EvaluationValidationError
from aiodoo_datasets.generators.evaluation.domain.evaluation import Evaluation


class DatasetValidator:
    """Validates complete evaluation datasets."""

    @staticmethod
    def validate(dataset: Tuple[Evaluation, ...]) -> None:
        """Fail-fast validation for the complete dataset."""
        seen_evaluation_ids = set()
        seen_suite_ids = set()
        seen_case_ids = set()
        seen_rule_ids = set()
        seen_output_ids = set()
        seen_ground_truth_ids = set()
        seen_references = set()

        for evaluation in dataset:
            if evaluation.evaluation_id in seen_evaluation_ids:
                raise EvaluationValidationError(
                    f"Duplicate Evaluation ID detected: {evaluation.evaluation_id}"
                )
            seen_evaluation_ids.add(evaluation.evaluation_id)

            # Check deterministic ordering of suites (e.g. by suite_id lexicographically)
            suite_ids = [suite.suite_id for suite in evaluation.catalog.suites]
            if suite_ids != sorted(suite_ids):
                raise EvaluationValidationError(
                    "BenchmarkSuites are not deterministically ordered."
                )

            for suite in evaluation.catalog.suites:
                if suite.suite_id in seen_suite_ids:
                    raise EvaluationValidationError(
                        f"Duplicate BenchmarkSuite ID detected: {suite.suite_id}"
                    )
                seen_suite_ids.add(suite.suite_id)

                # Check deterministic ordering of cases (e.g. by case_id lexicographically)
                case_ids = [case.case_id for case in suite.cases]
                if case_ids != sorted(case_ids):
                    raise EvaluationValidationError(
                        f"EvaluationCases in suite {suite.suite_id} are not deterministically ordered."
                    )

                for case in suite.cases:
                    if case.case_id in seen_case_ids:
                        raise EvaluationValidationError(
                            f"Duplicate EvaluationCase ID detected: {case.case_id}"
                        )
                    seen_case_ids.add(case.case_id)

                    if case.expected_output.output_id in seen_output_ids:
                        raise EvaluationValidationError(
                            f"Duplicate ExpectedOutput ID detected: {case.expected_output.output_id}"
                        )
                    seen_output_ids.add(case.expected_output.output_id)

                    if case.ground_truth.ground_truth_id in seen_ground_truth_ids:
                        raise EvaluationValidationError(
                            f"Duplicate GroundTruth ID detected: {case.ground_truth.ground_truth_id}"
                        )
                    seen_ground_truth_ids.add(case.ground_truth.ground_truth_id)

                    for rule in case.rules:
                        if rule.rule_id in seen_rule_ids:
                            raise EvaluationValidationError(
                                f"Duplicate Rule ID detected: {rule.rule_id}"
                            )
                        seen_rule_ids.add(rule.rule_id)

                    for ref in case.references:
                        ref_key = (ref.source_generator, ref.source_reference)
                        if ref_key in seen_references:
                            raise EvaluationValidationError(
                                f"Duplicate Reference detected: {ref_key}"
                            )
                        seen_references.add(ref_key)

                    # Validate score ranges
                    for score in case.scores:
                        if not (0 <= score.normalized_score <= 1.0):
                            raise EvaluationValidationError(
                                f"Score normalized_score out of range (0-1): {score.normalized_score}"
                            )
                        if score.weight < 0:
                            raise EvaluationValidationError(
                                f"Score weight cannot be negative: {score.weight}"
                            )
