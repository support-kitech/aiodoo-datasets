"""Coding parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from aiodoo_datasets.generators.conversation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.conversation.registries.parser_registry import ParserRegistry
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence
from aiodoo_datasets.generators.conversation.domain.reference import Reference
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment
from aiodoo_datasets.generators.conversation.enums import AttachmentType
import hashlib

@ParserRegistry.register("coding_protocol")
class CodingParser(BaseParser):
    """Parses Coding protocols."""
    
    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        attachments = []
        for file in data.get("files", []):
            file_id = file.get("file_id", "unknown")
            references.append(
                Reference(
                    source_generator="coding",
                    source_reference=file_id,
                    description=f"Generated file: {file.get('path', '')}"
                )
            )
            
            # Create a deterministic attachment id
            hash_input = f"CODE_ATT:{file_id}"
            att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
            
            attachments.append(
                Attachment(
                    attachment_id=f"ATT-{att_hash}",
                    attachment_type=AttachmentType.CODE,
                    content=file.get("content", ""),
                    file_path=file.get("path")
                )
            )
            
        return ExtractedEvidence(
            protocol_name="coding_protocol",
            references=tuple(references),
            attachments=tuple(attachments),
            raw_data=MappingProxyType(data)
        )
