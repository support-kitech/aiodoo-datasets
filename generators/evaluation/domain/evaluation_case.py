"""Evaluation Case domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple
from generators.evaluation.domain.metadata import EvaluationMetadata
from generators.evaluation.domain.reference import Reference
from generators.evaluation.domain.attachment import EvaluationAttachment
from generators.evaluation.domain.expected_output import ExpectedOutput
from generators.evaluation.domain.ground_truth import GroundTruth
from generators.evaluation.domain.evaluation_rule import EvaluationRule
from generators.evaluation.domain.success_criteria import SuccessCriteria
from generators.evaluation.domain.failure_criteria import FailureCriteria
from generators.evaluation.domain.score import EvaluationScore


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    """Immutable evaluation case representing a single test sample."""

    case_id: str
    prompt: str
    metadata: EvaluationMetadata
    expected_output: ExpectedOutput
    ground_truth: GroundTruth
    rules: Tuple[EvaluationRule, ...] = ()
    success_criteria: Tuple[SuccessCriteria, ...] = ()
    failure_criteria: Tuple[FailureCriteria, ...] = ()
    references: Tuple[Reference, ...] = ()
    attachments: Tuple[EvaluationAttachment, ...] = ()
    scores: Tuple[EvaluationScore, ...] = ()
