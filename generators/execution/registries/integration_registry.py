"""Static registry for integration pipeline components."""

from aiodoo_datasets.generators.execution.registries.base import BaseRegistry

class IntegrationRegistry(BaseRegistry):
    """
    Static registry for Integration pipeline stages.
    Inherits from BaseRegistry. Exposes validate() and snapshot().
    """

    def validate(self) -> None:
        """Validates execution order, duplicate stages, and missing stages."""
        types = set()
        for item in self._items:
            if item.__class__ in types:
                raise ValueError(f"Duplicate Integration stage registered: {item.__class__.__name__}")
            types.add(item.__class__)
