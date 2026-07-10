from abc import ABC, abstractmethod
from typing import Any

class BaseFactory(ABC):
    """
    Abstract interface for all Domain Factories.
    Enforces SOURCE/TARGET mappings and validation contracts.
    """
    
    SOURCE: Any
    TARGET: Any
    
    @abstractmethod
    def validate(self, knowledge: Any) -> None:
        """Validates upstream knowledge before instantiation to prevent silent failures."""
        pass
        
    @abstractmethod
    def create(self, knowledge: Any) -> Any:
        """Instantiates and returns the immutable TARGET domain object."""
        pass
