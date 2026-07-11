"""Domain model for a single engineering symbol in the Context Graph."""

import hashlib
from dataclasses import dataclass, field
from typing import Any, Optional

from generators.context.analysis.graph.enums import NodeType, LanguageType


@dataclass
class ContextNode:
    """Represents exactly one engineering symbol."""

    name: str
    module: str
    relative_path: str
    node_type: NodeType
    language: LanguageType
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    node_id: str = field(init=False)

    def __post_init__(self):  # type: ignore[no-untyped-def]
        # Generate a deterministic node_id
        hash_input = f"{self.module}:{self.relative_path}:{self.name}:{self.node_type.value}"
        if self.start_line is not None:
            hash_input += f":{self.start_line}"
        self.node_id = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ContextNode):
            return False
        return self.node_id == other.node_id

    def __hash__(self) -> int:
        return hash(self.node_id)

    def __lt__(self, other: "ContextNode") -> bool:
        # Deterministic sorting: path -> start_line -> node_id
        if self.relative_path != other.relative_path:
            return self.relative_path < other.relative_path

        # Handle None start lines by treating them as -1 for sorting
        self_line = self.start_line if self.start_line is not None else -1
        other_line = other.start_line if other.start_line is not None else -1
        if self_line != other_line:
            return self_line < other_line

        return self.node_id < other.node_id

    def to_dict(self) -> dict[str, Any]:
        """Deterministically serialize the node to a dictionary."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "name": self.name,
            "module": self.module,
            "relative_path": self.relative_path,
            "language": self.language.value,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "metadata": dict(sorted(self.metadata.items())),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextNode":
        """Deserialize from dictionary."""
        node = cls(
            name=data["name"],
            module=data["module"],
            relative_path=data["relative_path"],
            node_type=NodeType(data["node_type"]),
            language=LanguageType(data["language"]),
            start_line=data.get("start_line"),
            end_line=data.get("end_line"),
            metadata=data.get("metadata", {}),
        )
        # Override the generated node_id with the one from the dict if provided
        if "node_id" in data:
            node.node_id = data["node_id"]
        return node
