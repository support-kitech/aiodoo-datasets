"""Ground Truth Builder for Evaluation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.ground_truth import GroundTruth
from aiodoo_datasets.generators.evaluation.factories.ground_truth_factory import GroundTruthFactory

class GroundTruthBuilder:
    """Builds GroundTruth objects securely."""
    
    @staticmethod
    def build(case_id: str, exact_match_required: bool, keywords: Tuple[str, ...] = ()) -> GroundTruth:
        """Build ground truth."""
        return GroundTruthFactory.create(
            case_id=case_id,
            exact_match_required=exact_match_required,
            keywords=keywords
        )
