from aiodoo_datasets.generators.execution.registries.base import BaseRegistry


class FactoryRegistry(BaseRegistry):  # type: ignore[misc]
    """
    Validates and manages the mapping of Knowledge (SOURCE) to Domain (TARGET).
    """

    def validate(self) -> None:
        """
        Validates that factories don't have duplicate mapping declarations.
        """
        mappings = set()
        types = set()

        for factory in self._items:
            if factory.__class__ in types:
                raise ValueError(f"Duplicate Factory type registered: {factory.__class__.__name__}")
            types.add(factory.__class__)

            if not hasattr(factory, "SOURCE") or not hasattr(factory, "TARGET"):
                raise ValueError(f"{factory.__class__.__name__} missing SOURCE/TARGET declarations")

            mapping = (factory.SOURCE, factory.TARGET)
            if mapping in mappings:
                raise ValueError(
                    f"Duplicate factory mapping {mapping} found in {factory.__class__.__name__}"
                )
            mappings.add(mapping)
