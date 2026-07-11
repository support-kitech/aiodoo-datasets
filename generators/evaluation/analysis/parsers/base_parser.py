"""Base Parser for Evaluation Generator."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseParser(ABC):
    """Abstract base class for all protocol parsers."""

    @abstractmethod
    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Parse protocol into read-only deterministic extracted evidence."""
        pass
