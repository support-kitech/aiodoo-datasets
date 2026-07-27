"""Production generation policy constants for the Approval generator.

Locked by Step 2.1 Dataset Generation Policy. Do not introduce non-determinism.
"""

from __future__ import annotations

# Identity scheme for stable record_id derivation.
ID_SCHEME_VERSION: str = "1"

# Bounded evidence / findings written into each training record.
MAX_EVIDENCE_ITEMS: int = 32
MAX_FINDINGS: int = 32
MAX_RECOMMENDATIONS: int = 16
MAX_SNIPPET_CHARS: int = 200
MAX_DESCRIPTION_CHARS: int = 400
MAX_REASONING_CHARS: int = 2000

# Production SFT must never be a single-record placeholder.
MIN_PRODUCTION_RECORDS: int = 2

# Upstream capability → input_protocols key
CAPABILITY_DATA_KEYS: tuple[tuple[str, str], ...] = (
    ("planner", "planner_data"),
    ("coding", "coding_data"),
    ("repair", "repair_data"),
    ("execution", "execution_data"),
)
