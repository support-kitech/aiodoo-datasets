"""Dialogue slicing: one Conversation training example per assistant reply."""

from __future__ import annotations

from dataclasses import dataclass

from generators.conversation.analysis.episode import Episode
from generators.conversation.history import clip_message_content, truncate_prefix
from generators.conversation.identity import compute_record_id


@dataclass(frozen=True, slots=True)
class TrainingSlice:
    """One next-reply training unit."""

    conversation_id: str
    turn_index: int
    record_id: str
    module: str
    prefix: tuple[dict[str, str], ...]
    reply: dict[str, str]


class DialogueSlicer:
    """Slice an episode into one record per assistant reply."""

    @staticmethod
    def slice_episode(episode: Episode) -> tuple[TrainingSlice, ...]:
        messages = list(episode.messages)
        slices: list[TrainingSlice] = []
        assistant_ordinal = 0

        for idx, message in enumerate(messages):
            if message.role != "assistant":
                continue
            if not message.content.strip():
                continue

            raw_prefix = [{"role": m.role, "content": m.content} for m in messages[:idx]]
            prefix = truncate_prefix(raw_prefix)
            if not prefix:
                # Need at least one prior turn for ConversationRequest(min_length=1).
                continue

            reply = {
                "role": "assistant",
                "content": clip_message_content(message.content),
            }
            record_id = compute_record_id(episode.conversation_id, assistant_ordinal)
            slices.append(
                TrainingSlice(
                    conversation_id=episode.conversation_id,
                    turn_index=assistant_ordinal,
                    record_id=record_id,
                    module=episode.module,
                    prefix=tuple(prefix),
                    reply=reply,
                )
            )
            assistant_ordinal += 1

        return tuple(slices)

    @staticmethod
    def slice_many(episodes: tuple[Episode, ...]) -> tuple[TrainingSlice, ...]:
        out: list[TrainingSlice] = []
        seen: set[str] = set()
        for episode in episodes:
            for item in DialogueSlicer.slice_episode(episode):
                if item.record_id in seen:
                    continue
                seen.add(item.record_id)
                out.append(item)
        out.sort(key=lambda s: s.record_id)
        return tuple(out)
