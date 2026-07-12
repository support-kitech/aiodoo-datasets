"""Base parser for the Approval Generator."""

from abc import ABC, abstractmethod
from typing import Any, List
from generators.approval.domain.evidence import Evidence


class BaseParser(ABC):
    """Abstract base class for protocol evidence parsers."""

    @abstractmethod
    def parse(self, data: Any) -> List[Evidence]:
        """Parse raw upstream protocols into immutable Evidence objects."""
        pass
