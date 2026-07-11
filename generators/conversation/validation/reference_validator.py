"""Reference validator for Conversation Generator."""

from aiodoo_datasets.generators.conversation.exceptions import ConversationValidationError
from aiodoo_datasets.generators.conversation.domain.reference import Reference


class ReferenceValidator:
    """Validates structural integrity of a Reference."""

    @staticmethod
    def validate(reference: Reference) -> None:
        if not reference.source_generator:
            raise ConversationValidationError("Reference missing source_generator.")

        if not reference.source_reference:
            raise ConversationValidationError("Reference missing source_reference.")
