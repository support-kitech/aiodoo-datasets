"""Static registry for protocol components."""

from generators.execution.registries.base import BaseRegistry


class ProtocolRegistry(BaseRegistry):  # type: ignore[misc]
    """
    Static registry for Protocol Mappers, Protocol Validators, and Protocol Serializers.
    Inherits from BaseRegistry. Exposes validate() and snapshot().
    """

    def validate(self) -> None:
        """Validates no duplicate registrations exist."""
        types = set()
        for item in self._items:
            if item.__class__ in types:
                raise ValueError(
                    f"Duplicate Protocol component registered: {item.__class__.__name__}"
                )
            types.add(item.__class__)
