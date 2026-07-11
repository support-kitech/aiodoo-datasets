"""Execution parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from aiodoo_datasets.generators.conversation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.conversation.registries.parser_registry import ParserRegistry
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence
from aiodoo_datasets.generators.conversation.domain.reference import Reference
from aiodoo_datasets.generators.conversation.domain.attachment import Attachment
from aiodoo_datasets.generators.conversation.enums import AttachmentType
import hashlib


@ParserRegistry.register("execution_protocol")
class ExecutionParser(BaseParser):  # type: ignore[misc]
    """Parses Execution protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        attachments = []
        for result in data.get("test_results", []):
            result_id = result.get("test_id", "unknown")
            references.append(
                Reference(
                    source_generator="execution",
                    source_reference=result_id,
                    description=f"Execution result: {result.get('name', '')}",
                )
            )

            hash_input = f"LOG_ATT:{result_id}"
            att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

            attachments.append(
                Attachment(
                    attachment_id=f"ATT-{att_hash}",
                    attachment_type=AttachmentType.LOG,
                    content=result.get("log", ""),
                    file_path=None,
                )
            )

        return ExtractedEvidence(
            protocol_name="execution_protocol",
            references=tuple(references),
            attachments=tuple(attachments),
            raw_data=MappingProxyType(data),
        )
