"""Turn builder for Conversation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.conversation.domain.turn import Turn
from aiodoo_datasets.generators.conversation.domain.message import Message
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment
from aiodoo_datasets.generators.conversation.factories.turn_factory import TurnFactory


class TurnBuilder:
    """Builds Turn objects safely."""

    @staticmethod
    def build(
        conversation_id: str,
        sequence_index: int,
        messages: Tuple[Message, ...],
        attachments: Tuple[Attachment, ...] = (),
    ) -> Turn:
        return TurnFactory.create(
            conversation_id=conversation_id,
            sequence_index=sequence_index,
            messages=messages,
            attachments=attachments,
        )
