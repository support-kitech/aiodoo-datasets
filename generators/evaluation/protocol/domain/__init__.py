"""Protocol models for Evaluation Generator."""

from generators.evaluation.protocol.domain.evaluation_protocol import (
    MetadataProtocol,
    ExpectedOutputProtocol,
    GroundTruthProtocol,
    EvaluationRuleProtocol,
    SuccessCriteriaProtocol,
    FailureCriteriaProtocol,
    ReferenceProtocol,
    AttachmentProtocol,
    ScoreProtocol,
    EvaluationCaseProtocol,
)
from generators.evaluation.protocol.domain.benchmark_protocol import (
    BenchmarkMetadataProtocol,
    BenchmarkSuiteProtocol,
    BenchmarkCatalogProtocol,
    EvaluationProtocol,
)

__all__ = [
    "MetadataProtocol",
    "ExpectedOutputProtocol",
    "GroundTruthProtocol",
    "EvaluationRuleProtocol",
    "SuccessCriteriaProtocol",
    "FailureCriteriaProtocol",
    "ReferenceProtocol",
    "AttachmentProtocol",
    "ScoreProtocol",
    "EvaluationCaseProtocol",
    "BenchmarkMetadataProtocol",
    "BenchmarkSuiteProtocol",
    "BenchmarkCatalogProtocol",
    "EvaluationProtocol",
]
