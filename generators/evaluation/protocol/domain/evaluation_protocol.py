"""Evaluation Protocol models for Evaluation Generator."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Tuple, Optional

class MetadataProtocol(BaseModel):
    """Protocol for EvaluationMetadata."""
    model_config = ConfigDict(frozen=True)
    generator_version: str
    protocol_version: str
    schema_version: str
    source_module: str
    odoo_version: str
    odoo_edition: str
    evaluation_type: str
    difficulty: str
    complexity: int

class ExpectedOutputProtocol(BaseModel):
    """Protocol for ExpectedOutput."""
    model_config = ConfigDict(frozen=True)
    output_id: str
    expected_value: str
    value_type: str
    required_elements: Tuple[str, ...] = Field(default=())

class GroundTruthProtocol(BaseModel):
    """Protocol for GroundTruth."""
    model_config = ConfigDict(frozen=True)
    ground_truth_id: str
    exact_match_required: bool
    keywords: Tuple[str, ...] = Field(default=())

class EvaluationRuleProtocol(BaseModel):
    """Protocol for EvaluationRule."""
    model_config = ConfigDict(frozen=True)
    rule_id: str
    description: str
    rule_type: str
    parameters: Tuple[str, ...] = Field(default=())

class SuccessCriteriaProtocol(BaseModel):
    """Protocol for SuccessCriteria."""
    model_config = ConfigDict(frozen=True)
    criteria_id: str
    description: str
    weight: float

class FailureCriteriaProtocol(BaseModel):
    """Protocol for FailureCriteria."""
    model_config = ConfigDict(frozen=True)
    criteria_id: str
    description: str
    fatal: bool

class ReferenceProtocol(BaseModel):
    """Protocol for Reference."""
    model_config = ConfigDict(frozen=True)
    source_generator: str
    source_reference: str
    description: str

class AttachmentProtocol(BaseModel):
    """Protocol for EvaluationAttachment."""
    model_config = ConfigDict(frozen=True)
    attachment_id: str
    attachment_type: str
    content: str
    file_path: Optional[str] = None

class ScoreProtocol(BaseModel):
    """Protocol for EvaluationScore."""
    model_config = ConfigDict(frozen=True)
    score_id: str
    metric_name: str
    raw_score: float
    max_score: float
    normalized_score: float
    weight: float
    pass_threshold: float
    result: bool

class EvaluationCaseProtocol(BaseModel):
    """Protocol for EvaluationCase."""
    model_config = ConfigDict(frozen=True)
    case_id: str
    prompt: str
    metadata: MetadataProtocol
    expected_output: ExpectedOutputProtocol
    ground_truth: GroundTruthProtocol
    rules: Tuple[EvaluationRuleProtocol, ...] = Field(default=())
    success_criteria: Tuple[SuccessCriteriaProtocol, ...] = Field(default=())
    failure_criteria: Tuple[FailureCriteriaProtocol, ...] = Field(default=())
    references: Tuple[ReferenceProtocol, ...] = Field(default=())
    attachments: Tuple[AttachmentProtocol, ...] = Field(default=())
    scores: Tuple[ScoreProtocol, ...] = Field(default=())
