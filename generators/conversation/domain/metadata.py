"""Metadata domain model for Conversation Generator."""

from dataclasses import dataclass
from generators.conversation.enums import ConversationType


@dataclass(frozen=True, slots=True)
class ConversationMetadata:
    """Immutable environment and context tracking for a conversation."""

    generator_version: str
    protocol_version: str
    schema_version: str
    source_module: str
    odoo_version: str
    odoo_edition: str
    language: str
    complexity: int
    conversation_type: ConversationType
