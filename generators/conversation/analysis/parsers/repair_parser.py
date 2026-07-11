"""Repair parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from aiodoo_datasets.generators.conversation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.conversation.registries.parser_registry import ParserRegistry
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence
from aiodoo_datasets.generators.conversation.domain.reference import Reference
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment
from aiodoo_datasets.generators.conversation.enums import AttachmentType
import hashlib


@ParserRegistry.register("repair_protocol")
class RepairParser(BaseParser):
    """Parses Repair protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        attachments = []
        for patch in data.get("patches", []):
            patch_id = patch.get("patch_id", "unknown")
            references.append(
                Reference(
                    source_generator="repair",
                    source_reference=patch_id,
                    description=f"Repair patch: {patch.get('description', '')}",
                )
            )

            hash_input = f"DIFF_ATT:{patch_id}"
            att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

            attachments.append(
                Attachment(
                    attachment_id=f"ATT-{att_hash}",
                    attachment_type=AttachmentType.DIFF,
                    content=patch.get("diff", ""),
                    file_path=patch.get("file_path"),
                )
            )

        return ExtractedEvidence(
            protocol_name="repair_protocol",
            references=tuple(references),
            attachments=tuple(attachments),
            raw_data=MappingProxyType(data),
        )
