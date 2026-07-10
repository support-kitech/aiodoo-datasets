from abc import ABC, abstractmethod
from typing import Any

class BaseRegistry(ABC):
    """
    Abstract interface for all plugin registries (Builders, Factories).
    """
    
    def __init__(self):
        self._items = []
        
    def register(self, item: Any) -> None:
        """Registers a new item."""
        self._items.append(item)
        
    def unregister(self, item: Any) -> None:
        """Removes an item."""
        if item in self._items:
            self._items.remove(item)
            
    @abstractmethod
    def validate(self) -> None:
        """Validates the state of the registry before execution."""
        pass
        
    def items(self) -> tuple[Any, ...]:
        """Returns the registered items."""
        return tuple(self._items)
        
    def snapshot(self) -> tuple[Any, ...]:
        """Returns an immutable snapshot of the registry state."""
        return tuple(self._items)
