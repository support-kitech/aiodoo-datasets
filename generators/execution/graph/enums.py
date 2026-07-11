"""Graph-specific enums."""

from enum import Enum, auto


class NodeType(Enum):
    """Classification of a node within the execution graph."""

    STEP = auto()
    OPERATION = auto()
    ARTIFACT = auto()


class EdgeType(Enum):
    """Classification of an edge relationship."""

    DEPENDENCY = auto()
    SEQUENCE = auto()
    ROLLBACK = auto()


class TraversalStrategy(Enum):
    """Supported graph traversal algorithms."""

    DFS = auto()
    BFS = auto()
    REVERSE = auto()
    DEPENDENCY = auto()
    ROLLBACK = auto()
