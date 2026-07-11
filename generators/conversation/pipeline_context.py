"""Pipeline context for Conversation Generator."""

from dataclasses import dataclass
from typing import Dict, Any
from aiodoo_datasets.generators.conversation.domain.metadata import ConversationMetadata

@dataclass(frozen=True)
class PipelineContext:
    """Immutable configuration and inputs for the pipeline."""
    input_protocols: Dict[str, Dict[str, Any]]
    metadata: ConversationMetadata
    output_dir: str
    source_identifier: str
    strict_mode: bool = True
