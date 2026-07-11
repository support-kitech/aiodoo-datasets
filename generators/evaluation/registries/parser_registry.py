"""Parser Registry for Evaluation Generator."""

from typing import Dict, Any
from types import MappingProxyType

class ParserRegistry:
    """Static registry for Evaluation Parsers."""
    
    _parsers: Dict[str, Any] = {}
    _frozen: bool = False
    
    @classmethod
    def register(cls, source_type: str, parser_class: Any) -> None:
        """Register a parser statically."""
        if cls._frozen:
            raise RuntimeError("ParserRegistry is frozen and cannot be modified.")
        cls._parsers[source_type] = parser_class
        
    @classmethod
    def get(cls, source_type: str) -> Any:
        """Retrieve a parser by source type."""
        return cls._parsers.get(source_type)

    @classmethod
    def freeze(cls) -> None:
        """Freeze the registry to prevent further modification."""
        cls._frozen = True

    @classmethod
    def get_all(cls) -> MappingProxyType:
        """Return a read-only mapping of all registered parsers."""
        return MappingProxyType(cls._parsers)
