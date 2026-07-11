"""Turn domain model for Conversation Generator."""

from dataclasses import dataclass
from typing import Tuple
from generators.conversation.domain.message import Message
from generators.conversation.domain.attachment import Attachment


@dataclass(frozen=True, slots=True)
class Turn:
    """A logical interaction boundary of messages and context."""

    turn_id: str
    messages: Tuple[Message, ...]
    attachments: Tuple[Attachment, ...] = ()
