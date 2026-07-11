"""Turn factory for the Conversation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.conversation.domain.turn import Turn
from aiodoo_datasets.generators.conversation.domain.message import Message
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment


class TurnFactory:
    """Factory for creating immutable Turn objects with deterministic IDs."""

    @staticmethod
    def generate_id(conversation_id: str, sequence_index: int) -> str:
        """Generate a deterministic turn ID."""
        hash_input = f"TURN:{conversation_id}:{sequence_index}"
        turn_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"TRN-{turn_hash}"

    @staticmethod
    def create(
        conversation_id: str,
        sequence_index: int,
        messages: Tuple[Message, ...],
        attachments: Tuple[Attachment, ...] = (),
    ) -> Turn:
        """Create a new turn with a hash-based deterministic ID."""
        turn_id = TurnFactory.generate_id(conversation_id, sequence_index)

        return Turn(turn_id=turn_id, messages=messages, attachments=attachments)
