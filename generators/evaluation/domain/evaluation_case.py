"""Evaluation Case domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.reference import Reference
from aiodoo_datasets.generators.evaluation.domain.attachment import EvaluationAttachment
from aiodoo_datasets.generators.evaluation.domain.expected_output import ExpectedOutput
from aiodoo_datasets.generators.evaluation.domain.ground_truth import GroundTruth
from aiodoo_datasets.generators.evaluation.domain.evaluation_rule import EvaluationRule
from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria
from aiodoo_datasets.generators.evaluation.domain.score import EvaluationScore

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
