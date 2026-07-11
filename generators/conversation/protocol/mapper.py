"""Protocol mapper for Conversation Generator."""

from aiodoo_datasets.generators.conversation.domain.conversation import Conversation
from aiodoo_datasets.generators.conversation.domain.turn import Turn
from aiodoo_datasets.generators.conversation.domain.message import Message
from aiodoo_datasets.generators.conversation.domain.reference import Reference
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment
from aiodoo_datasets.generators.conversation.domain.metadata import ConversationMetadata

from aiodoo_datasets.generators.conversation.protocol.domain.conversation_protocol import (
    ConversationProtocol, MetadataProtocol, TurnProtocol, MessageProtocol, 
    AttachmentProtocol, ReferenceProtocol
)

class ProtocolMapper:
    """Maps immutable domain models to strict Pydantic protocols."""
    
    @staticmethod
    def map_reference(ref: Reference) -> ReferenceProtocol:
        return ReferenceProtocol(
            source_generator=ref.source_generator,
            source_reference=ref.source_reference,
            description=ref.description
        )
        
    @staticmethod
    def map_attachment(att: Attachment) -> AttachmentProtocol:
        return AttachmentProtocol(
            attachment_id=att.attachment_id,
            attachment_type=att.attachment_type,
            content=att.content,
            file_path=att.file_path
        )
        
    @staticmethod
    def map_message(msg: Message) -> MessageProtocol:
        return MessageProtocol(
            message_id=msg.message_id,
            role=msg.role,
            content=msg.content,
            references=[ProtocolMapper.map_reference(r) for r in msg.references]
        )
        
    @staticmethod
    def map_turn(turn: Turn) -> TurnProtocol:
        return TurnProtocol(
            turn_id=turn.turn_id,
            messages=[ProtocolMapper.map_message(m) for m in turn.messages],
            attachments=[ProtocolMapper.map_attachment(a) for a in turn.attachments]
        )
        
    @staticmethod
    def map_metadata(meta: ConversationMetadata) -> MetadataProtocol:
        return MetadataProtocol(
            generator_version=meta.generator_version,
            protocol_version=meta.protocol_version,
            schema_version=meta.schema_version,
            source_module=meta.source_module,
            odoo_version=meta.odoo_version,
            odoo_edition=meta.odoo_edition,
            language=meta.language,
            complexity=meta.complexity,
            conversation_type=meta.conversation_type
        )
        
    @staticmethod
    def map_conversation(conv: Conversation) -> ConversationProtocol:
        return ConversationProtocol(
            conversation_id=conv.conversation_id,
            metadata=ProtocolMapper.map_metadata(conv.metadata),
            turns=[ProtocolMapper.map_turn(t) for t in conv.turns]
        )
