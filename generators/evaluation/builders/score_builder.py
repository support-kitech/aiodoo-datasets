"""Score Builder for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.score import EvaluationScore
from aiodoo_datasets.generators.evaluation.factories.score_factory import ScoreFactory

class ScoreBuilder:
    """Builds EvaluationScore objects securely."""
    
    @staticmethod
    def build(
        case_id: str,
        metric_name: str,
        raw_score: float,
        max_score: float,
        normalized_score: float,
        weight: float,
        pass_threshold: float,
        result: bool
    ) -> EvaluationScore:
        """Build evaluation score."""
        return ScoreFactory.create(
            case_id=case_id,
            metric_name=metric_name,
            raw_score=raw_score,
            max_score=max_score,
            normalized_score=normalized_score,
            weight=weight,
            pass_threshold=pass_threshold,
            result=result
        )
