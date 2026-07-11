"""Statistics tracking for Conversation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.common.statistics.base_statistics import BaseStatistics
from aiodoo_datasets.generators.conversation.protocol.domain.conversation_protocol import (
    ConversationProtocol,
)


class ConversationStatistics(BaseStatistics):  # type: ignore[misc]
    """Tracks metrics for the Conversation Generator."""

    def __init__(self) -> None:
        super().__init__()
        self.conversations_generated = 0
        self.turns_generated = 0
        self.messages_generated = 0
        self.conversation_types: Dict[str, int] = {}

    def add_sample(self, protocol: ConversationProtocol) -> None:
        """Add metrics from a generated protocol."""
        self.conversations_generated += 1

        c_type = protocol.metadata.conversation_type.value
        self.conversation_types[c_type] = self.conversation_types.get(c_type, 0) + 1

        self.turns_generated += len(protocol.turns)
        for turn in protocol.turns:
            self.messages_generated += len(turn.messages)

    def get_summary(self) -> Dict[str, Any]:
        """Return the tracked metrics."""
        summary = super().get_summary()
        summary.update(
            {
                "conversations_generated": self.conversations_generated,
                "turns_generated": self.turns_generated,
                "messages_generated": self.messages_generated,
                "average_turns_per_conversation": self.turns_generated
                / max(1, self.conversations_generated),
                "average_messages_per_turn": self.messages_generated / max(1, self.turns_generated),
                "conversation_types": self.conversation_types,
            }
        )
        return summary  # type: ignore[no-any-return]
