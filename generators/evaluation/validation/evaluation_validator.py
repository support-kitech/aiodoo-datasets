"""Evaluation Validator for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.exceptions import EvaluationValidationError
from aiodoo_datasets.generators.evaluation.domain.evaluation import Evaluation
from aiodoo_datasets.generators.evaluation.validation.benchmark_validator import BenchmarkValidator

class EvaluationValidator:
    """Validates the root Evaluation aggregate."""
    
    @staticmethod
    def validate(evaluation: Evaluation) -> None:
        """Fail-fast validation."""
        if not evaluation.evaluation_id.startswith("EVALROOT-"):
            raise EvaluationValidationError(f"Invalid Evaluation root ID: {evaluation.evaluation_id}")
            
        if not evaluation.catalog:
            raise EvaluationValidationError("Evaluation must contain a BenchmarkCatalog.")
            
        BenchmarkValidator.validate_catalog(evaluation.catalog)
