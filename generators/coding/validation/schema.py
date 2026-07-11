"""Strict schemas for the Coding Dataset JSONL format using Pydantic."""

from typing import Any
from enum import Enum
from pydantic import BaseModel, Field


class OperationType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    PATCH = "PATCH"
    RENAME = "RENAME"


class ArtifactType(str, Enum):
    FILE = "file"
    COMMAND = "command"
    CONFIG = "config"


class LanguageType(str, Enum):
    PYTHON = "python"
    XML = "xml"
    JAVASCRIPT = "javascript"
    CSS = "css"
    SCSS = "scss"
    CSV = "csv"
    YAML = "yaml"
    JSON = "json"
    TEXT = "text"


class ValidationStatus(str, Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    FAILED = "failed"


class ArtifactStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class GeneratedArtifact(BaseModel):
    id: str
    type: ArtifactType
    language: LanguageType
    path: str
    intent: str
    reason: str
    created_by: str
    diff: str = ""
    status: ArtifactStatus = ArtifactStatus.PENDING
    version: int = 1
    dependencies: list[str] = Field(default_factory=list)
    validation_status: ValidationStatus = ValidationStatus.PENDING


class FileOperation(BaseModel):
    operation: OperationType
    path: str
    intent: str = ""
    reason: str = ""


class ValidationAction(BaseModel):
    action: str
    reason: str


class ArtifactPayload(BaseModel):
    goal: str
    workspace: str
    artifacts: list[GeneratedArtifact]
    operations: list[FileOperation]
    validation_actions: list[ValidationAction]
    summary: str


class CodingDatasetRecord(BaseModel):
    """The overall JSONL row structure for the Coding Generator."""

    instruction: str
    context: dict[str, Any]
    output: ArtifactPayload
    metadata: dict[str, Any]
