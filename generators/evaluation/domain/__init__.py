"""Domain models for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.evaluation import Evaluation
from aiodoo_datasets.generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from aiodoo_datasets.generators.evaluation.domain.reference import Reference
from aiodoo_datasets.generators.evaluation.domain.attachment import EvaluationAttachment
from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria
from aiodoo_datasets.generators.evaluation.domain.evaluation_rule import EvaluationRule
from aiodoo_datasets.generators.evaluation.domain.expected_output import ExpectedOutput
from aiodoo_datasets.generators.evaluation.domain.ground_truth import GroundTruth
from aiodoo_datasets.generators.evaluation.domain.score import EvaluationScore
from aiodoo_datasets.generators.evaluation.domain.category import Category
from aiodoo_datasets.generators.evaluation.domain.evaluation_case import EvaluationCase
from aiodoo_datasets.generators.evaluation.domain.benchmark_suite import BenchmarkSuite
from aiodoo_datasets.generators.evaluation.domain.future import ModelComparison, PreferenceEvaluation, HumanReview, RewardModel

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
