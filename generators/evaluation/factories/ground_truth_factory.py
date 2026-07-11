"""Ground Truth Factory for Evaluation Generator."""

import hashlib
from typing import Tuple
from generators.evaluation.domain.ground_truth import GroundTruth


class GroundTruthFactory:
    """Factory for creating immutable GroundTruth objects with deterministic IDs."""

    @staticmethod
    def generate_id(case_id: str) -> str:
        """Generate a deterministic ground truth ID."""
        hash_input = f"TRUTH:{case_id}"
        truth_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"TRUTH-{truth_hash}"

    @staticmethod
    def create(
        case_id: str, exact_match_required: bool, keywords: Tuple[str, ...] = ()
    ) -> GroundTruth:
        """Create a new ground truth with a hash-based deterministic ID."""
        ground_truth_id = GroundTruthFactory.generate_id(case_id)

        return GroundTruth(
            ground_truth_id=ground_truth_id,
            exact_match_required=exact_match_required,
            keywords=keywords,
        )
