"""Builder Registry for Evaluation Generator."""

from typing import Dict, Any
from types import MappingProxyType

class BuilderRegistry:
    """Static registry for Evaluation Builders."""
    
    _builders: Dict[str, Any] = {}
    _frozen: bool = False
    
    @classmethod
    def register(cls, builder_name: str, builder_class: Any) -> None:
        """Register a builder statically."""
        if cls._frozen:
            raise RuntimeError("BuilderRegistry is frozen and cannot be modified.")
        cls._builders[builder_name] = builder_class
        
    @classmethod
    def get(cls, builder_name: str) -> Any:
        """Retrieve a builder by name."""
        return cls._builders.get(builder_name)

    @classmethod
    def freeze(cls) -> None:
        """Freeze the registry to prevent further modification."""
        cls._frozen = True

    @classmethod
    def get_all(cls) -> MappingProxyType:
        """Return a read-only mapping of all registered builders."""
        return MappingProxyType(cls._builders)
