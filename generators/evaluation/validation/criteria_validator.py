"""Criteria Validator for Evaluation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.evaluation.exceptions import EvaluationValidationError
from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria

class CriteriaValidator:
    """Validates SuccessCriteria and FailureCriteria."""
    
    @staticmethod
    def validate_success(criteria: Tuple[SuccessCriteria, ...]) -> None:
        """Fail-fast validation."""
        for c in criteria:
            if not c.criteria_id.startswith("SUCC-"):
                raise EvaluationValidationError(f"Invalid SuccessCriteria ID: {c.criteria_id}")
            if c.weight < 0:
                raise EvaluationValidationError("SuccessCriteria weight cannot be negative.")

    @staticmethod
    def validate_failure(criteria: Tuple[FailureCriteria, ...]) -> None:
        """Fail-fast validation."""
        for c in criteria:
            if not c.criteria_id.startswith("FAIL-"):
                raise EvaluationValidationError(f"Invalid FailureCriteria ID: {c.criteria_id}")
