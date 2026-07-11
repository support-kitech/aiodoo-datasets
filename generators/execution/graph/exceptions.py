"""Graph-specific exception hierarchy."""


class GraphError(Exception):
    """Base exception for all graph-related failures."""

    pass


class CycleDetectedError(GraphError):
    """Raised when a circular dependency is detected in the graph."""

    def __init__(self, cycles: tuple[tuple[str, ...], ...], message: str = "") -> None:
        self.cycles = cycles
        super().__init__(message or f"Cycle(s) detected: {cycles}")


class InvalidEdgeError(GraphError):
    """Raised when an edge references a non-existent node or is a self-loop."""

    pass


class InvalidNodeError(GraphError):
    """Raised when a node has invalid or duplicate identifiers."""

    pass


class GraphValidationError(GraphError):
    """Raised when the graph fails structural validation."""

    pass
