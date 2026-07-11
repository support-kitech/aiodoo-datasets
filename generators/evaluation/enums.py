"""Enums for Evaluation Generator."""

from enum import Enum


class EvaluationType(str, Enum):
    """Types of evaluations supported by the generator."""

    PLANNING = "planning"
    CODING = "coding"
    REPAIR = "repair"
    CONTEXT = "context"
    EXECUTION = "execution"
    APPROVAL = "approval"
    CONVERSATION = "conversation"
    CROSS_MODULE = "cross_module"
    REGRESSION = "regression"
    INTEGRATION = "integration"


class BenchmarkCategory(str, Enum):
    """Categories for benchmark suites."""

    CORE = "core"
    QUALITY = "quality"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ARCHITECTURE = "architecture"


class DifficultyLevel(str, Enum):
    """Difficulty levels for evaluation cases."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class AttachmentType(str, Enum):
    """Types of attachments associated with evaluation."""

    CODE = "code"
    DIFF = "diff"
    LOG = "log"
    DOCUMENT = "document"
    TRACE = "trace"
