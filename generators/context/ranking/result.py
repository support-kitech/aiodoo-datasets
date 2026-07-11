"""Domain model for Ranking Results."""

import hashlib
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from aiodoo_datasets.generators.context.ranking.enums import (
    RankingRuleType,
    RankingScore,
    RankingReason,
)


@dataclass(frozen=True)
class RankingResult:
    """Represents a deterministic ranked connection between a Query and a Node."""

    query_id: str
    node_id: str
    score: RankingScore
    matched_rule: RankingRuleType
    reason: RankingReason
    metadata: MappingProxyType[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    # Internal fields for tie-breaking sort (populated from metadata during init)
    _relative_path: str = field(init=False, repr=False, compare=False)
    _start_line: int = field(init=False, repr=False, compare=False)
    result_id: str = field(init=False)

    def __post_init__(self):
        # Extract tie-breaking context if provided, default to empty/0
        object.__setattr__(self, "_relative_path", self.metadata.get("relative_path", ""))
        object.__setattr__(self, "_start_line", self.metadata.get("start_line", 0))

        # Generate deterministic result_id
        hash_input = f"{self.query_id}:{self.node_id}:{self.matched_rule.value}"
        object.__setattr__(
            self, "result_id", hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RankingResult):
            return False
        # Task 5: Equality based only on query_id, node_id, matched_rule
        return (
            self.query_id == other.query_id
            and self.node_id == other.node_id
            and self.matched_rule == other.matched_rule
        )

    def __hash__(self) -> int:
        return hash((self.query_id, self.node_id, self.matched_rule))

    def __lt__(self, other: "RankingResult") -> bool:
        """
        Deterministic Ordering:
        score DESC -> node_id ASC -> relative_path ASC -> start_line ASC
        """
        if self.score != other.score:
            return self.score > other.score  # Higher score comes FIRST
        if self.node_id != other.node_id:
            return self.node_id < other.node_id
        if self._relative_path != other._relative_path:
            return self._relative_path < other._relative_path
        if self._start_line != other._start_line:
            return self._start_line < other._start_line

        return self.result_id < other.result_id

    def to_dict(self) -> dict[str, Any]:
        """Deterministically serialize the ranking result."""
        return {
            "result_id": self.result_id,
            "query_id": self.query_id,
            "node_id": self.node_id,
            "score": self.score.value,
            "matched_rule": self.matched_rule.value,
            "reason": self.reason.value,
            "metadata": dict(sorted(self.metadata.items())),
        }
