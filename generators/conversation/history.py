"""History truncation for Conversation training prefixes."""

from __future__ import annotations

from typing import Sequence

from generators.conversation.policy import (
    MAX_HISTORY_CHARS,
    MAX_HISTORY_MESSAGES,
    MAX_MESSAGE_CHARS,
)


def clip_message_content(content: str, *, limit: int = MAX_MESSAGE_CHARS) -> str:
    text = content.strip()
    if len(text) <= limit:
        return text
    return text[:limit]


def truncate_prefix(
    messages: Sequence[dict[str, str]],
    *,
    max_messages: int = MAX_HISTORY_MESSAGES,
    max_chars: int = MAX_HISTORY_CHARS,
) -> list[dict[str, str]]:
    """Keep the most recent prefix messages under turn and char budgets.

    Never includes messages after the reply (caller must pass prefix only).
    Deterministic: always drops from the front (oldest first).
    """
    clipped = [
        {
            "role": str(m.get("role", "")),
            "content": clip_message_content(str(m.get("content", ""))),
        }
        for m in messages
        if str(m.get("role", "")).strip() and str(m.get("content", "")).strip()
    ]
    if not clipped:
        return []

    # Message-count budget from the end.
    limited = clipped[-max(0, max_messages) :] if max_messages > 0 else []

    # Char budget from the end.
    total = 0
    kept_rev: list[dict[str, str]] = []
    for message in reversed(limited):
        size = len(message["content"])
        if kept_rev and total + size > max_chars:
            break
        kept_rev.append(message)
        total += size
    kept_rev.reverse()
    return kept_rev
