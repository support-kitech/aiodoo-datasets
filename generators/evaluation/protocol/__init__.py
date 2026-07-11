"""Protocol Layer for Evaluation Generator."""

from generators.evaluation.protocol.mapper import ProtocolMapper
from generators.evaluation.protocol.domain import (
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
    BenchmarkMetadataProtocol,
    BenchmarkSuiteProtocol,
    BenchmarkCatalogProtocol,
    EvaluationProtocol,
)

__all__ = [
    "ProtocolMapper",
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
