"""Rule Builder for Evaluation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.evaluation_rule import EvaluationRule
from aiodoo_datasets.generators.evaluation.factories.rule_factory import RuleFactory

class RuleBuilder:
    """Builds EvaluationRule objects securely."""
    
    @staticmethod
    def build(case_id: str, sequence_index: int, description: str, rule_type: str, parameters: Tuple[str, ...] = ()) -> EvaluationRule:
        """Build evaluation rule."""
        return RuleFactory.create(
            case_id=case_id,
            sequence_index=sequence_index,
            description=description,
            rule_type=rule_type,
            parameters=parameters
        )
