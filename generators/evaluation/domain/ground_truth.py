"""Ground Truth domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class GroundTruth:
    """Immutable ground truth representation for evaluation matching."""

    ground_truth_id: str
    exact_match_required: bool
    keywords: Tuple[str, ...]
