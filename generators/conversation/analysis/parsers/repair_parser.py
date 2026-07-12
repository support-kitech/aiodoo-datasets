"""Repair parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference
from generators.conversation.domain.attachment import Attachment
from generators.conversation.enums import AttachmentType
import hashlib


@ParserRegistry.register("repair_protocol")
class RepairParser(BaseParser):  # type: ignore[misc]
    """Parses Repair protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        attachments = []
        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            output = record.get("output", {})
            tasks = output.get("tasks", []) if isinstance(output, dict) else []
            record_ref = record.get("metadata", {}).get("protocol_hash", "repair")
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                patch_id = task.get("id", "unknown")
                source_ref = f"{record_ref}:{patch_id}"
                references.append(
                    Reference(
                        source_generator="repair",
                        source_reference=source_ref,
                        description=f"Repair task: {task.get('problem', {})}",
                    )
                )

                hash_input = f"DIFF_ATT:{source_ref}"
                att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

                attachments.append(
                    Attachment(
                        attachment_id=f"ATT-{att_hash}",
                        attachment_type=AttachmentType.DIFF,
                        content=str(task.get("expected_outcome", ""))[:500],
                        file_path=None,
                    )
                )
                if len(references) >= 25:
                    break
            if len(references) >= 25:
                break

        return ExtractedEvidence(
            protocol_name="repair_protocol",
            references=tuple(references),
            attachments=tuple(attachments),
            raw_data=MappingProxyType({"record_count": len(records)}),
        )
