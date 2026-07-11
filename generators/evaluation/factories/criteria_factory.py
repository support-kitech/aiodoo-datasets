"""Criteria Factory for Evaluation Generator."""

import hashlib
from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria


class CriteriaFactory:
    """Factory for creating immutable Criteria objects."""

    @staticmethod
    def generate_success_id(case_id: str, sequence_index: int) -> str:
        """Generate a deterministic success criteria ID."""
        hash_input = f"SUCC:{case_id}:{sequence_index}"
        crit_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"SUCC-{crit_hash}"

    @staticmethod
    def generate_failure_id(case_id: str, sequence_index: int) -> str:
        """Generate a deterministic failure criteria ID."""
        hash_input = f"FAIL:{case_id}:{sequence_index}"
        crit_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"FAIL-{crit_hash}"

    @staticmethod
    def create_success(
        case_id: str, sequence_index: int, description: str, weight: float
    ) -> SuccessCriteria:
        """Create a success criteria with a deterministic ID."""
        criteria_id = CriteriaFactory.generate_success_id(case_id, sequence_index)
        return SuccessCriteria(criteria_id=criteria_id, description=description, weight=weight)

    @staticmethod
    def create_failure(
        case_id: str, sequence_index: int, description: str, fatal: bool
    ) -> FailureCriteria:
        """Create a failure criteria with a deterministic ID."""
        criteria_id = CriteriaFactory.generate_failure_id(case_id, sequence_index)
        return FailureCriteria(criteria_id=criteria_id, description=description, fatal=fatal)
