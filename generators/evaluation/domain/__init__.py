"""Domain models for Evaluation Generator."""

from generators.evaluation.domain.evaluation import Evaluation
from generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from generators.evaluation.domain.metadata import EvaluationMetadata
from generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from generators.evaluation.domain.reference import Reference
from generators.evaluation.domain.attachment import EvaluationAttachment
from generators.evaluation.domain.success_criteria import SuccessCriteria
from generators.evaluation.domain.failure_criteria import FailureCriteria
from generators.evaluation.domain.evaluation_rule import EvaluationRule
from generators.evaluation.domain.expected_output import ExpectedOutput
from generators.evaluation.domain.ground_truth import GroundTruth
from generators.evaluation.domain.score import EvaluationScore
from generators.evaluation.domain.category import Category
from generators.evaluation.domain.evaluation_case import EvaluationCase
from generators.evaluation.domain.benchmark_suite import BenchmarkSuite
from generators.evaluation.domain.future import (
    ModelComparison,
    PreferenceEvaluation,
    HumanReview,
    RewardModel,
)

__all__ = [
    "Evaluation",
    "BenchmarkCatalog",
    "EvaluationMetadata",
    "BenchmarkMetadata",
    "Reference",
    "EvaluationAttachment",
    "SuccessCriteria",
    "FailureCriteria",
    "EvaluationRule",
    "ExpectedOutput",
    "GroundTruth",
    "EvaluationScore",
    "Category",
    "EvaluationCase",
    "BenchmarkSuite",
    "ModelComparison",
    "PreferenceEvaluation",
    "HumanReview",
    "RewardModel",
]
