"""Protocol validator for Conversation Generator."""

from aiodoo_datasets.generators.conversation.exceptions import ConversationValidationError
from aiodoo_datasets.generators.conversation.protocol.domain.conversation_protocol import (
    ConversationProtocol,
)


class ProtocolValidator:
    """Validates protocol serialization layer."""

    @staticmethod
    def validate(protocol: ConversationProtocol) -> None:
        # Pydantic validation handles most schema checks.
        # This acts as a wrapper for additional custom integrity checks.
        if not protocol.conversation_id:
            raise ConversationValidationError("Protocol missing conversation_id.")
