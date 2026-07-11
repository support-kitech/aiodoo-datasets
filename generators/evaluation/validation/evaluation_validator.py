"""Evaluation Validator for Evaluation Generator."""

from generators.evaluation.exceptions import EvaluationValidationError
from generators.evaluation.domain.evaluation import Evaluation
from generators.evaluation.validation.benchmark_validator import BenchmarkValidator


class EvaluationValidator:
    """Validates the root Evaluation aggregate."""

    @staticmethod
    def validate(evaluation: Evaluation) -> None:
        """Fail-fast validation."""
        if not evaluation.evaluation_id.startswith("EVALROOT-"):
            raise EvaluationValidationError(
                f"Invalid Evaluation root ID: {evaluation.evaluation_id}"
            )

        if not evaluation.catalog:
            raise EvaluationValidationError("Evaluation must contain a BenchmarkCatalog.")

        BenchmarkValidator.validate_catalog(evaluation.catalog)
