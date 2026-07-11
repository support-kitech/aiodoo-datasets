"""Base parser for Conversation Generator."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence


class BaseParser(ABC):
    """Abstract base class for protocol parsers."""

    @abstractmethod
    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        """Extract evidence and references from the raw protocol data."""
        pass
