"""Protocol domain model for Conversation Generator."""

from pydantic import BaseModel, Field
from typing import List, Optional
from aiodoo_datasets.generators.conversation.enums import Role, AttachmentType, ConversationType


class ReferenceProtocol(BaseModel):
    source_generator: str
    source_reference: str
    description: str


class AttachmentProtocol(BaseModel):
    attachment_id: str
    attachment_type: AttachmentType
    content: str
    file_path: Optional[str] = None


class MessageProtocol(BaseModel):
    message_id: str
    role: Role
    content: str
    references: List[ReferenceProtocol] = Field(default_factory=list)


class TurnProtocol(BaseModel):
    turn_id: str
    messages: List[MessageProtocol]
    attachments: List[AttachmentProtocol] = Field(default_factory=list)


class MetadataProtocol(BaseModel):
    generator_version: str
    protocol_version: str
    schema_version: str
    source_module: str
    odoo_version: str
    odoo_edition: str
    language: str
    complexity: int
    conversation_type: ConversationType


class ConversationProtocol(BaseModel):
    conversation_id: str
    metadata: MetadataProtocol
    turns: List[TurnProtocol]
