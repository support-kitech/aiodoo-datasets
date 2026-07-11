"""Difficulty Estimator for Evaluation Generator."""

from typing import Dict, Any


class DifficultyEstimator:
    """Deterministically estimates the difficulty level of the extracted evidence."""

    @staticmethod
    def estimate(evidence: Dict[str, Any]) -> str:
        """Estimate difficulty purely based on structural evidence."""
        # This is a deterministic heuristic
        if "complex_feature" in evidence:
            return "hard"
        return "medium"
