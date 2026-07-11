"""Evaluation Case Factory for Evaluation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.evaluation_case import EvaluationCase
from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.expected_output import ExpectedOutput
from aiodoo_datasets.generators.evaluation.domain.ground_truth import GroundTruth
from aiodoo_datasets.generators.evaluation.domain.evaluation_rule import EvaluationRule
from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria
from aiodoo_datasets.generators.evaluation.domain.reference import Reference
from aiodoo_datasets.generators.evaluation.domain.attachment import EvaluationAttachment
from aiodoo_datasets.generators.evaluation.domain.score import EvaluationScore


class EvaluationCaseFactory:
    """Factory for creating immutable EvaluationCase objects with deterministic IDs."""

    @staticmethod
    def generate_id(suite_id: str, sequence_index: int) -> str:
        """Generate a deterministic case ID."""
        hash_input = f"CASE:{suite_id}:{sequence_index}"
        case_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"CASE-{case_hash}"

    @staticmethod
    def create(
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
        """Create a new evaluation case with a hash-based deterministic ID."""
        case_id = EvaluationCaseFactory.generate_id(suite_id, sequence_index)

        return EvaluationCase(
            case_id=case_id,
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
