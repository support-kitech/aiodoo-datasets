"""Conversation factory for the Conversation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.conversation.domain.conversation import Conversation
from aiodoo_datasets.generators.conversation.domain.metadata import ConversationMetadata
from aiodoo_datasets.generators.conversation.domain.turn import Turn

class ConversationFactory:
    """Factory for creating immutable Conversation objects with deterministic IDs."""
    
    @staticmethod
    def generate_id(conversation_type: str, source_identifier: str) -> str:
        """Generate a deterministic conversation ID."""
        hash_input = f"CONV:{conversation_type}:{source_identifier}"
        conv_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"CONV-{conv_hash}"
    
    @staticmethod
    def create(metadata: ConversationMetadata, turns: Tuple[Turn, ...], source_identifier: str) -> Conversation:
        """Create a new conversation with a hash-based deterministic ID."""
        conversation_id = ConversationFactory.generate_id(metadata.conversation_type.value, source_identifier)
        
        return Conversation(
            conversation_id=conversation_id,
            metadata=metadata,
            turns=turns
        )
