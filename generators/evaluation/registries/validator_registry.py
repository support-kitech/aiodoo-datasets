"""Validator Registry for Evaluation Generator."""

from typing import Dict, Any
from types import MappingProxyType


class ValidatorRegistry:
    """Static registry for Evaluation Validators."""

    _validators: Dict[str, Any] = {}
    _frozen: bool = False

    @classmethod
    def register(cls, validator_name: str, validator_class: Any) -> None:
        """Register a validator statically."""
        if cls._frozen:
            raise RuntimeError("ValidatorRegistry is frozen and cannot be modified.")
        cls._validators[validator_name] = validator_class

    @classmethod
    def get(cls, validator_name: str) -> Any:
        """Retrieve a validator by name."""
        return cls._validators.get(validator_name)

    @classmethod
    def freeze(cls) -> None:
        """Freeze the registry to prevent further modification."""
        cls._frozen = True

    @classmethod
    def get_all(cls) -> MappingProxyType:  # type: ignore[type-arg]
        """Return a read-only mapping of all registered validators."""
        return MappingProxyType(cls._validators)
