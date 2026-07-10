"""Message domain model for Conversation Generator."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.conversation.enums import Role
from aiodoo_datasets.generators.conversation.domain.reference import Reference

@dataclass(frozen=True, slots=True)
class Message:
    """A single immutable utterance bounded to a role."""
    message_id: str
    role: Role
    content: str
    references: Tuple[Reference, ...] = ()
