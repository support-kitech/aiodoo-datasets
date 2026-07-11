"""Expected Output domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class ExpectedOutput:
    """Immutable target response for evaluation."""

    output_id: str
    expected_value: str
    value_type: str
    required_elements: Tuple[str, ...] = ()
