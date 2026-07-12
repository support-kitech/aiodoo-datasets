"""Coding parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference
from generators.conversation.domain.attachment import Attachment
from generators.conversation.enums import AttachmentType
import hashlib


@ParserRegistry.register("coding_protocol")
class CodingParser(BaseParser):  # type: ignore[misc]
    """Parses Coding protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        attachments = []
        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            output = record.get("output", {})
            artifacts = output.get("artifacts", []) if isinstance(output, dict) else []
            record_ref = record.get("metadata", {}).get("protocol_hash", "coding")
            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    continue
                file_id = artifact.get("id", "unknown")
                source_ref = f"{record_ref}:{file_id}"
                references.append(
                    Reference(
                        source_generator="coding",
                        source_reference=source_ref,
                        description=f"Generated artifact: {artifact.get('path', '')}",
                    )
                )

                hash_input = f"CODE_ATT:{source_ref}"
                att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

                attachments.append(
                    Attachment(
                        attachment_id=f"ATT-{att_hash}",
                        attachment_type=AttachmentType.CODE,
                        content=str(artifact.get("intent", ""))[:500],
                        file_path=artifact.get("path"),
                    )
                )
                if len(references) >= 25:
                    break
            if len(references) >= 25:
                break

        return ExtractedEvidence(
            protocol_name="coding_protocol",
            references=tuple(references),
            attachments=tuple(attachments),
            raw_data=MappingProxyType({"record_count": len(records)}),
        )
