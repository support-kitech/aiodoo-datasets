"""Production generation policy for the Evaluation generator (Step 2.1)."""

from __future__ import annotations

ID_SCHEME_VERSION: str = "1"

MIN_PRODUCTION_RECORDS: int = 2

# Required upstream for SFT judgments (Approval/Conversation soft until regenerated).
REQUIRED_SOURCE_TYPES: tuple[str, ...] = (
    "planner",
    "coding",
    "repair",
    "execution",
)

OPTIONAL_SOURCE_TYPES: tuple[str, ...] = (
    "context",
    "approval",
    "conversation",
)

# Cap oversized supporting corpora (deterministic: first N after sort).
MAX_RECORDS_PER_CAPABILITY: dict[str, int] = {
    "context": 256,
}

# Verdict mix bands (informational; generator always emits pass+fail pairs).
PASS_CASE_KEY: str = "pass"
FAIL_CASE_KEY: str = "fail"
INCONCLUSIVE_CASE_KEY: str = "inconclusive"
