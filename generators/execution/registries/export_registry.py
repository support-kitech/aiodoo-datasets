"""Static registry for export components."""

from aiodoo_datasets.generators.execution.registries.base import BaseRegistry


class ExportRegistry(BaseRegistry):
    """
    Static registry for Writers, Export Validators, and Export Hooks.
    Inherits from BaseRegistry. Exposes validate() and snapshot().
    """

    def validate(self) -> None:
        """Validates no duplicate registrations exist."""
        types = set()
        for item in self._items:
            if item.__class__ in types:
                raise ValueError(
                    f"Duplicate Export component registered: {item.__class__.__name__}"
                )
            types.add(item.__class__)
