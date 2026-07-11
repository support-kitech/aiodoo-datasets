"""Message builder for Conversation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.conversation.domain.message import Message
from aiodoo_datasets.generators.conversation.enums import Role
from aiodoo_datasets.generators.conversation.domain.reference import Reference
from aiodoo_datasets.generators.conversation.factories.message_factory import MessageFactory


class MessageBuilder:
    """Builds Message objects safely."""

    @staticmethod
    def build(
        role: Role,
        content: str,
        turn_id: str,
        sequence_index: int,
        references: Tuple[Reference, ...] = (),
    ) -> Message:
        return MessageFactory.create(
            role=role,
            content=content,
            turn_id=turn_id,
            sequence_index=sequence_index,
            references=references,
        )
