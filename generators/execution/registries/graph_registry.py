"""Static registry for graph components."""

from generators.execution.registries.base import BaseRegistry


class GraphRegistry(BaseRegistry):  # type: ignore[misc]
    """
    Static registry for Graph Builders, Graph Validators, and Graph Traversals.

    Inherits from BaseRegistry. Exposes validate() and snapshot().
    """

    def validate(self) -> None:
        """Validates no duplicate registrations exist."""
        types = set()
        for item in self._items:
            if item.__class__ in types:
                raise ValueError(f"Duplicate Graph component registered: {item.__class__.__name__}")
            types.add(item.__class__)
