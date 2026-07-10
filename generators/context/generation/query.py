"""Domain model for engineering queries."""

import hashlib
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent

@dataclass(frozen=True)
class Query:
    """Represents a single, deterministic engineering question."""
    query_type: QueryType
    intent: QueryIntent
    target_node: str  # The node_id this query originates from or targets
    target_symbol: str # The human-readable symbol (e.g., model name, field name)
    natural_language: str
    metadata: MappingProxyType[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    query_id: str = field(init=False)

    def __post_init__(self):
        # Generate deterministic query_id from immutable properties
        hash_input = f"{self.query_type.value}:{self.intent.value}:{self.target_symbol}:{self.target_node}"
        # object.__setattr__ must be used because the dataclass is frozen
        object.__setattr__(self, 'query_id', hashlib.sha256(hash_input.encode("utf-8")).hexdigest())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Query):
            return False
        return self.query_id == other.query_id

    def __hash__(self) -> int:
        return hash(self.query_id)

    def __lt__(self, other: "Query") -> bool:
        # Deterministic sorting: query_type -> target_symbol -> query_id
        if self.query_type.value != other.query_type.value:
            return self.query_type.value < other.query_type.value
        if self.target_symbol != other.target_symbol:
            return self.target_symbol < other.target_symbol
        return self.query_id < other.query_id

    def to_dict(self) -> dict[str, Any]:
        """Deterministically serialize the query."""
        return {
            "query_id": self.query_id,
            "query_type": self.query_type.value,
            "intent": self.intent.value,
            "target_node": self.target_node,
            "target_symbol": self.target_symbol,
            "natural_language": self.natural_language,
            "metadata": dict(sorted(self.metadata.items()))
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Query":
        """Deserialize from dictionary."""
        q = cls(
            query_type=QueryType(data["query_type"]),
            intent=QueryIntent(data["intent"]),
            target_node=data["target_node"],
            target_symbol=data["target_symbol"],
            natural_language=data["natural_language"],
            metadata=MappingProxyType(data.get("metadata", {}))
        )
        if "query_id" in data:
            object.__setattr__(q, 'query_id', data["query_id"])
        return q
