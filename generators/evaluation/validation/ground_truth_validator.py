"""Ground Truth Validator for Evaluation Generator."""

from generators.evaluation.exceptions import EvaluationValidationError
from generators.evaluation.domain.ground_truth import GroundTruth
from generators.evaluation.domain.expected_output import ExpectedOutput


class GroundTruthValidator:
    """Validates GroundTruth and ExpectedOutput consistency deterministically."""

    @staticmethod
    def validate(ground_truth: GroundTruth, expected_output: ExpectedOutput) -> None:
        """Fail-fast validation."""
        if not ground_truth.ground_truth_id.startswith("TRUTH-"):
            raise EvaluationValidationError(
                f"Invalid GroundTruth ID prefix: {ground_truth.ground_truth_id}"
            )

        if not expected_output.output_id.startswith("EXPOUT-"):
            raise EvaluationValidationError(
                f"Invalid ExpectedOutput ID prefix: {expected_output.output_id}"
            )

        if ground_truth.exact_match_required and not expected_output.expected_value:
            raise EvaluationValidationError("Exact match requires a non-empty expected value.")
