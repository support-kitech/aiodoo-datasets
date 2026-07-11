"""Criteria Builder for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria
from aiodoo_datasets.generators.evaluation.factories.criteria_factory import CriteriaFactory

class CriteriaBuilder:
    """Builds Criteria objects securely."""
    
    @staticmethod
    def build_success(case_id: str, sequence_index: int, description: str, weight: float) -> SuccessCriteria:
        """Build success criteria."""
        return CriteriaFactory.create_success(
            case_id=case_id,
            sequence_index=sequence_index,
            description=description,
            weight=weight
        )
        
    @staticmethod
    def build_failure(case_id: str, sequence_index: int, description: str, fatal: bool) -> FailureCriteria:
        """Build failure criteria."""
        return CriteriaFactory.create_failure(
            case_id=case_id,
            sequence_index=sequence_index,
            description=description,
            fatal=fatal
        )
