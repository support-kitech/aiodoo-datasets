"""Static registry for planning components."""

from aiodoo_datasets.generators.execution.registries.base import BaseRegistry


class PlanningRegistry(BaseRegistry):  # type: ignore[misc]
    """
    Static registry for Stage Builders, Planning Strategies, and Scheduling Strategies.
    Inherits from BaseRegistry. Exposes validate() and snapshot().
    """

    def validate(self) -> None:
        """Validates no duplicate registrations exist."""
        types = set()
        for item in self._items:
            if item.__class__ in types:
                raise ValueError(
                    f"Duplicate Planning component registered: {item.__class__.__name__}"
                )
            types.add(item.__class__)
