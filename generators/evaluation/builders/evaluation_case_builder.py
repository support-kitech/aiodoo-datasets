"""Evaluation Case Builder for Evaluation Generator."""

from typing import Tuple
from generators.evaluation.domain.evaluation_case import EvaluationCase
from generators.evaluation.domain.metadata import EvaluationMetadata
from generators.evaluation.domain.expected_output import ExpectedOutput
from generators.evaluation.domain.ground_truth import GroundTruth
from generators.evaluation.domain.evaluation_rule import EvaluationRule
from generators.evaluation.domain.success_criteria import SuccessCriteria
from generators.evaluation.domain.failure_criteria import FailureCriteria
from generators.evaluation.domain.reference import Reference
from generators.evaluation.domain.attachment import EvaluationAttachment
from generators.evaluation.domain.score import EvaluationScore
from generators.evaluation.factories.evaluation_case_factory import (
    EvaluationCaseFactory,
)


class EvaluationCaseBuilder:
    """Orchestrates the construction of an EvaluationCase."""

    @staticmethod
    def build(
        suite_id: str,
        sequence_index: int,
        prompt: str,
        metadata: EvaluationMetadata,
        expected_output: ExpectedOutput,
        ground_truth: GroundTruth,
        rules: Tuple[EvaluationRule, ...] = (),
        success_criteria: Tuple[SuccessCriteria, ...] = (),
        failure_criteria: Tuple[FailureCriteria, ...] = (),
        references: Tuple[Reference, ...] = (),
        attachments: Tuple[EvaluationAttachment, ...] = (),
        scores: Tuple[EvaluationScore, ...] = (),
    ) -> EvaluationCase:
        """Build an evaluation case by orchestrating the factory."""
        return EvaluationCaseFactory.create(
            suite_id=suite_id,
            sequence_index=sequence_index,
            prompt=prompt,
            metadata=metadata,
            expected_output=expected_output,
            ground_truth=ground_truth,
            rules=rules,
            success_criteria=success_criteria,
            failure_criteria=failure_criteria,
            references=references,
            attachments=attachments,
            scores=scores,
        )
