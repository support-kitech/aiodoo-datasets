"""Metadata builder for Conversation Generator."""

from aiodoo_datasets.generators.conversation.domain.metadata import ConversationMetadata
from aiodoo_datasets.generators.conversation.enums import ConversationType
import json

class MetadataBuilder:
    """Builds standard conversation metadata from generator environment."""
    
    @staticmethod
    def build(conversation_type: ConversationType, source_module: str, language: str = "en", complexity: int = 1) -> ConversationMetadata:
        from aiodoo_datasets.generators.conversation.version import __version__, SCHEMA_VERSION
        
        return ConversationMetadata(
            generator_version=__version__,
            protocol_version="1.0",
            schema_version=SCHEMA_VERSION,
            source_module=source_module,
            odoo_version="18.0",
            odoo_edition="enterprise",
            language=language,
            complexity=complexity,
            conversation_type=conversation_type
        )
