"""Domain model for a relationship between two engineering symbols."""

import hashlib
from dataclasses import dataclass, field
from typing import Any

from generators.context.analysis.graph.enums import RelationshipType


@dataclass
class ContextEdge:
    """Represents a directed relationship between two ContextNodes."""

    source_id: str
    target_id: str
    relationship_type: RelationshipType
    metadata: dict[str, Any] = field(default_factory=dict)
    edge_id: str = field(init=False)

    def __post_init__(self):  # type: ignore[no-untyped-def]
        # Generate a deterministic edge_id
        hash_input = f"{self.source_id}:{self.target_id}:{self.relationship_type.value}"
        self.edge_id = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ContextEdge):
            return False
        return self.edge_id == other.edge_id

    def __hash__(self) -> int:
        return hash(self.edge_id)

    def __lt__(self, other: "ContextEdge") -> bool:
        # Deterministic sorting: source -> target -> relationship
        if self.source_id != other.source_id:
            return self.source_id < other.source_id
        if self.target_id != other.target_id:
            return self.target_id < other.target_id
        return self.relationship_type.value < other.relationship_type.value  # type: ignore[no-any-return]

    def to_dict(self) -> dict[str, Any]:
        """Deterministically serialize the edge to a dictionary."""
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "metadata": dict(sorted(self.metadata.items())),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextEdge":
        """Deserialize from dictionary."""
        edge = cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            relationship_type=RelationshipType(data["relationship_type"]),
            metadata=data.get("metadata", {}),
        )
        # Override generated edge_id if provided
        if "edge_id" in data:
            edge.edge_id = data["edge_id"]
        return edge
