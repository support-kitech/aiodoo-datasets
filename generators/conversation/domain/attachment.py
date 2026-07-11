"""Attachment domain model for Conversation Generator."""

from dataclasses import dataclass
from typing import Optional
from generators.conversation.enums import AttachmentType


@dataclass(frozen=True, slots=True)
class Attachment:
    """File, code snippet, or context attached to a turn."""

    attachment_id: str
    attachment_type: AttachmentType
    content: str
    file_path: Optional[str] = None
