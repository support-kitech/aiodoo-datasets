"""Conversation validator for Conversation Generator."""

from generators.conversation.exceptions import ConversationValidationError
from generators.conversation.domain.conversation import Conversation
from generators.conversation.validation.message_validator import MessageValidator
from generators.conversation.validation.reference_validator import (
    ReferenceValidator,
)


class ConversationValidator:
    """Validates full conversation domain model."""

    @staticmethod
    def validate(conversation: Conversation) -> None:
        if not conversation.conversation_id.startswith("CONV-"):
            raise ConversationValidationError(
                f"Invalid conversation ID format: {conversation.conversation_id}"
            )

        if not conversation.turns:
            raise ConversationValidationError(
                f"Conversation {conversation.conversation_id} has no turns."
            )

        for turn in conversation.turns:
            if not turn.turn_id.startswith("TRN-"):
                raise ConversationValidationError(f"Invalid turn ID format: {turn.turn_id}")

            for message in turn.messages:
                MessageValidator.validate(message)
                for ref in message.references:
                    ReferenceValidator.validate(ref)
