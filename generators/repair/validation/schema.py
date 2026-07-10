"""Strict schemas for the Repair Dataset JSONL format using Pydantic."""

from typing import Any
from enum import Enum
from pydantic import BaseModel, Field

class RepairSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ArtifactType(str, Enum):
    PYTHON = "python"
    XML = "xml"
    MANIFEST = "manifest"
    SECURITY = "security"
    DATA = "data"

class Problem(BaseModel):
    description: str
    severity: RepairSeverity
    location: str

class RootCause(BaseModel):
    analysis: str

class Artifact(BaseModel):
    id: str
    path: str
    type: ArtifactType
    start_line: int | None = None
    end_line: int | None = None
    content: str
    
class RepairOperation(BaseModel):
    operation: str
    search: str
    replace: str

class ExpectedOutcome(BaseModel):
    operations: list[RepairOperation]
    explanation: str

class RepairTask(BaseModel):
    id: str
    problem: Problem
    root_cause: RootCause
    context: list[Artifact] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    expected_outcome: ExpectedOutcome
    constraints: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class RepairPayload(BaseModel):
    goal: str
    workspace: str
    tasks: list[RepairTask]
    summary: str

class RepairDatasetRecord(BaseModel):
    """The overall JSONL row structure for the Repair Generator."""
    instruction: str
    context: dict[str, Any]
    output: RepairPayload
    metadata: dict[str, Any]
