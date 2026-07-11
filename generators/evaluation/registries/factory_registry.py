"""Factory Registry for Evaluation Generator."""

from typing import Dict, Any
from types import MappingProxyType

class FactoryRegistry:
    """Static registry for Evaluation Factories."""
    
    _factories: Dict[str, Any] = {}
    _frozen: bool = False
    
    @classmethod
    def register(cls, factory_name: str, factory_class: Any) -> None:
        """Register a factory statically."""
        if cls._frozen:
            raise RuntimeError("FactoryRegistry is frozen and cannot be modified.")
        cls._factories[factory_name] = factory_class
        
    @classmethod
    def get(cls, factory_name: str) -> Any:
        """Retrieve a factory by name."""
        return cls._factories.get(factory_name)

    @classmethod
    def freeze(cls) -> None:
        """Freeze the registry to prevent further modification."""
        cls._frozen = True

    @classmethod
    def get_all(cls) -> MappingProxyType:
        """Return a read-only mapping of all registered factories."""
        return MappingProxyType(cls._factories)
