"""Message factory for the Conversation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.conversation.domain.message import Message
from aiodoo_datasets.generators.conversation.enums import Role
from aiodoo_datasets.generators.conversation.domain.reference import Reference

class MessageFactory:
    """Factory for creating immutable Message objects with deterministic IDs."""
    
    @staticmethod
    def create(role: Role, content: str, turn_id: str, sequence_index: int, references: Tuple[Reference, ...] = ()) -> Message:
        """Create a new message with a hash-based deterministic ID."""
        hash_input = f"MSG:{turn_id}:{sequence_index}:{role.value}:{content[:50]}"
        msg_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        message_id = f"MSG-{msg_hash}"
        
        return Message(
            message_id=message_id,
            role=role,
            content=content,
            references=references
        )
