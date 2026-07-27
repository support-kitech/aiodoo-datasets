"""Statistics tracking for Conversation Generator."""

from __future__ import annotations

from typing import Any, Dict

from generators.common.statistics.base_statistics import BaseStatistics


class ConversationStatistics(BaseStatistics):  # type: ignore[misc]
    """Tracks metrics for the Conversation Generator."""

    def __init__(self) -> None:
        super().__init__()
        self.conversations_generated = 0
        self.episodes_generated = 0
        self.training_examples = 0
        self.turns_generated = 0
        self.messages_generated = 0
        self.conversation_types: Dict[str, int] = {}
        self._seen_conversation_ids: set[str] = set()

    def add_sample(self, protocol: Any, json_str: str) -> None:
        """Add metrics from a generated training record."""
        if isinstance(protocol, dict):

            class _Record:
                def __init__(self, metadata: Dict[str, Any]) -> None:
                    self.metadata = metadata

            metadata = protocol.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            self._add_base_sample(_Record(metadata), json_str)
            self.training_examples += 1

            conversation_id = protocol.get("conversation_id") or metadata.get("conversation_id")
            if isinstance(conversation_id, str) and conversation_id:
                if conversation_id not in self._seen_conversation_ids:
                    self._seen_conversation_ids.add(conversation_id)
                    self.conversations_generated = len(self._seen_conversation_ids)

            c_type = str(metadata.get("conversation_type", "unknown"))
            self.conversation_types[c_type] = self.conversation_types.get(c_type, 0) + 1

            output = protocol.get("output", {})
            turns = output.get("turns", []) if isinstance(output, dict) else []
            self.turns_generated += len(turns)
            for turn in turns:
                if isinstance(turn, dict):
                    self.messages_generated += len(turn.get("messages", []))
            return

        self._add_base_sample(protocol, json_str)
        self.training_examples += 1
        self.conversations_generated += 1

    def get_export_stats(self) -> dict[str, Any]:
        return {
            "conversations_generated": self.conversations_generated,
            "episodes_generated": self.episodes_generated or self.conversations_generated,
            "training_examples": self.training_examples or self.total_samples,
            "turns_generated": self.turns_generated,
            "messages_generated": self.messages_generated,
            "average_turns_per_example": self.turns_generated / max(1, self.total_samples),
            "average_messages_per_turn": self.messages_generated / max(1, self.turns_generated),
            "conversation_types": dict(self.conversation_types),
        }
