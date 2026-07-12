"""Statistics tracking for Conversation Generator."""

from typing import Dict, Any
from generators.common.statistics.base_statistics import BaseStatistics


class ConversationStatistics(BaseStatistics):  # type: ignore[misc]
    """Tracks metrics for the Conversation Generator."""

    def __init__(self) -> None:
        super().__init__()
        self.conversations_generated = 0
        self.turns_generated = 0
        self.messages_generated = 0
        self.conversation_types: Dict[str, int] = {}

    def add_sample(self, protocol: Any, json_str: str) -> None:
        """Add metrics from a generated protocol."""
        if isinstance(protocol, dict):

            class _Record:
                def __init__(self, metadata: Dict[str, Any]) -> None:
                    self.metadata = metadata

            self._add_base_sample(_Record(protocol.get("metadata", {})), json_str)
            self.conversations_generated += 1
            output = protocol.get("output", {})
            metadata = protocol.get("metadata", {})
            c_type = str(metadata.get("conversation_type", "unknown"))
            self.conversation_types[c_type] = self.conversation_types.get(c_type, 0) + 1
            turns = output.get("turns", []) if isinstance(output, dict) else []
            self.turns_generated += len(turns)
            for turn in turns:
                if isinstance(turn, dict):
                    self.messages_generated += len(turn.get("messages", []))
            return

        self._add_base_sample(protocol, json_str)
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
