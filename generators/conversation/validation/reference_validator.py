"""Reference validator for Conversation Generator."""

from generators.conversation.exceptions import ConversationValidationError
from generators.conversation.domain.reference import Reference


class ReferenceValidator:
    """Validates structural integrity of a Reference."""

    @staticmethod
    def validate(reference: Reference) -> None:
        if not reference.source_generator:
            raise ConversationValidationError("Reference missing source_generator.")

        if not reference.source_reference:
            raise ConversationValidationError("Reference missing source_reference.")
