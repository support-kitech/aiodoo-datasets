"""Dataset validator for Conversation Generator."""

from typing import List
from generators.conversation.exceptions import ConversationValidationError
from generators.conversation.protocol.domain.conversation_protocol import (
    ConversationProtocol,
)


class DatasetValidator:
    """Validates dataset-wide consistency across multiple protocols."""

    @staticmethod
    def validate_all(protocols: List[ConversationProtocol]) -> None:
        seen_ids = set()
        for p in protocols:
            if p.conversation_id in seen_ids:
                raise ConversationValidationError(
                    f"Duplicate conversation_id found in dataset: {p.conversation_id}"
                )
            seen_ids.add(p.conversation_id)
