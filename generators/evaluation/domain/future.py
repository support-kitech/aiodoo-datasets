"""Future placeholders for Evaluation Generator."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelComparison:
    """Placeholder for future Model vs Model comparison evaluation structure."""

    pass


@dataclass(frozen=True, slots=True)
class PreferenceEvaluation:
    """Placeholder for future Preference evaluation structure."""

    pass


@dataclass(frozen=True, slots=True)
class HumanReview:
    """Placeholder for future Human Review evaluation structure."""

    pass


@dataclass(frozen=True, slots=True)
class RewardModel:
    """Placeholder for future Reward Model training structures."""

    pass
