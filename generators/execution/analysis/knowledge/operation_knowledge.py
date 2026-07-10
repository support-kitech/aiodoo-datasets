"""Operation knowledge container."""

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, eq=True)
class OperationKnowledge:
    """Extracted intent to manipulate an artifact."""
    artifact_ref_id: str
    action_type: str
    diff_payload: str | None = None
    raw_metadata: dict[str, Any] | None = None
