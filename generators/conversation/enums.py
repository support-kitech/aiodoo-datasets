"""Enumerations for the Conversation Generator."""

from enum import Enum

class ConversationType(str, Enum):
    """Supported conversation types."""
    PLANNING = "planning"
    CODING = "coding"
    REPAIR = "repair"
    CONTEXT = "context"
    EXECUTION = "execution"
    APPROVAL = "approval"
    EVALUATION = "evaluation"
    AGENT = "agent"
    HUMAN_REVIEW = "human_review"

class Role(str, Enum):
    """Supported message roles."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    REVIEWER = "reviewer"

class AttachmentType(str, Enum):
    """Supported attachment types within a turn."""
    CODE = "code"
    DIFF = "diff"
    LOG = "log"
    DOCUMENTATION = "documentation"
