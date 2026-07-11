"""Message validator for Conversation Generator."""

from generators.conversation.exceptions import ConversationValidationError
from generators.conversation.domain.message import Message


class MessageValidator:
    """Validates structural integrity of a Message."""

    @staticmethod
    def validate(message: Message) -> None:
        if not message.message_id.startswith("MSG-"):
            raise ConversationValidationError(f"Invalid message ID format: {message.message_id}")

        if not message.content:
            raise ConversationValidationError(f"Message {message.message_id} has empty content.")
