"""Analysis result for Conversation Generator."""

from dataclasses import dataclass
from typing import Tuple, Any
from types import MappingProxyType
from aiodoo_datasets.generators.conversation.domain.reference import Reference
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment

@dataclass(frozen=True, slots=True)
class ExtractedEvidence:
    """A container for extracted protocol features."""
    protocol_name: str
    references: Tuple[Reference, ...]
    attachments: Tuple[Attachment, ...]
    raw_data: MappingProxyType[str, Any] # Contains the raw context mapped

@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Immutable map of extracted context from all upstream protocols."""
    evidence_pool: Tuple[ExtractedEvidence, ...]
