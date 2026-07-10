"""Enums for the domain layer."""

from enum import Enum

class OperationAction(Enum):
    """The engineering intent applied to the artifact."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class ConstraintType(Enum):
    """The nature of the constraint."""
    ENVIRONMENT = "environment"
    DEPENDENCY = "dependency"
    EDITION = "edition"
    VERSION = "version"
    CUSTOM = "custom"

class VerificationType(Enum):
    """How the verification is executed."""
    COMMAND = "command"
    PYTHON = "python"
    SQL = "sql"
    HTTP = "http"

class RollbackType(Enum):
    """How the rollback is executed."""
    COMMAND = "command"
    PYTHON = "python"
    SQL = "sql"

class StepStatus(Enum):
    """The lifecycle status of a step during execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
