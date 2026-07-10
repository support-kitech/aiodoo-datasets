"""Conversation domain model for Conversation Generator."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.conversation.domain.metadata import ConversationMetadata
from aiodoo_datasets.generators.conversation.domain.turn import Turn

@dataclass(frozen=True, slots=True)
class Conversation:
    """Immutable sequence of turns making up a full generated conversation."""
    conversation_id: str
    metadata: ConversationMetadata
    turns: Tuple[Turn, ...]
