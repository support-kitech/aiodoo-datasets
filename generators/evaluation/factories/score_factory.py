"""Score Factory for Evaluation Generator."""

import hashlib
from aiodoo_datasets.generators.evaluation.domain.score import EvaluationScore

class ScoreFactory:
    """Factory for creating immutable EvaluationScore objects."""
    
    @staticmethod
    def generate_id(case_id: str, metric_name: str) -> str:
        """Generate a deterministic score ID."""
        hash_input = f"SCORE:{case_id}:{metric_name}"
        score_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"SCORE-{score_hash}"

    @staticmethod
    def create(
        case_id: str,
        metric_name: str,
        raw_score: float,
        max_score: float,
        normalized_score: float,
        weight: float,
        pass_threshold: float,
        result: bool
    ) -> EvaluationScore:
        """Create an evaluation score with a hash-based deterministic ID."""
        score_id = ScoreFactory.generate_id(case_id, metric_name)
        return EvaluationScore(
            score_id=score_id,
            metric_name=metric_name,
            raw_score=raw_score,
            max_score=max_score,
            normalized_score=normalized_score,
            weight=weight,
            pass_threshold=pass_threshold,
            result=result
        )
