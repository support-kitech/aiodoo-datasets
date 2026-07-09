"""Strict Protocol V1 validation schemas using Pydantic."""

from typing import Any
from pydantic import BaseModel, Field

class Analysis(BaseModel):
    summary: str
    risks: list[str] = Field(default_factory=list)

class GeneratedArtifact(BaseModel):
    id: str
    type: str
    language: str
    path: str
    content: str
    reason: str
    created_by: str
    diff: str = ""
    status: str = "pending"
    version: int = 1
    dependencies: list[str] = Field(default_factory=list)
    validation_status: str = "pending"

class TaskSpec(BaseModel):
    id: str
    title: str
    description: str
    priority: str = "medium"
    status: str = "pending"
    complexity: int
    dependencies: list[str] = Field(default_factory=list)
    estimated_files: int
    estimated_time: int
    retry_count: int = 0
    assigned_model: str = ""
    generated_artifacts: list[GeneratedArtifact] = Field(default_factory=list)
    execution_result: dict[str, Any] = Field(default_factory=dict)
    phase: str = ""

class PlanAction(BaseModel):
    id: str
    action: str
    args: dict[str, Any]
    reason: str
    expected_result: str
    depends_on: list[str] = Field(default_factory=list)
    continue_on_error: bool = False

class PlanPayload(BaseModel):
    goal: str
    workspace: str
    analysis: Analysis
    tasks: list[TaskSpec]
    execution: list[PlanAction]
    summary: str

class PlannerDatasetRecord(BaseModel):
    """The overall JSONL row structure."""
    instruction: str
    input: str
    output: PlanPayload
    metadata: dict[str, Any]
