"""Production generation policy for the Conversation generator (Step 2.1)."""

from __future__ import annotations

ID_SCHEME_VERSION: str = "1"

# Bounded history written into each training request prefix.
MAX_HISTORY_MESSAGES: int = 16
MAX_HISTORY_CHARS: int = 12_000
MAX_MESSAGE_CHARS: int = 1_500

# Production SFT must never be a single integrated-conversation placeholder.
MIN_PRODUCTION_RECORDS: int = 2

# Architectural required upstream (Approval is soft / optional).
REQUIRED_PROTOCOL_KEYS: tuple[str, ...] = (
    "planner_protocol",
    "coding_protocol",
    "execution_protocol",
)

OPTIONAL_PROTOCOL_KEYS: tuple[str, ...] = (
    "repair_protocol",
    "context_protocol",
    "approval_protocol",
)

# Protocol key → capability label used in dialogue reconstruction.
PROTOCOL_CAPABILITY: dict[str, str] = {
    "planner_protocol": "planner",
    "coding_protocol": "coding",
    "repair_protocol": "repair",
    "execution_protocol": "execution",
    "context_protocol": "context",
    "approval_protocol": "approval",
}
