"""Execution parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference
from generators.conversation.domain.attachment import Attachment
from generators.conversation.enums import AttachmentType
import hashlib


@ParserRegistry.register("execution_protocol")
class ExecutionParser(BaseParser):  # type: ignore[misc]
    """Parses Execution protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        attachments = []
        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            output = record.get("output", {})
            steps = output.get("steps", []) if isinstance(output, dict) else []
            execution_id = (
                output.get("execution_id", "execution") if isinstance(output, dict) else "execution"
            )
            for step in steps:
                if not isinstance(step, dict):
                    continue
                result_id = f"{execution_id}:{step.get('id', 'unknown')}"
                references.append(
                    Reference(
                        source_generator="execution",
                        source_reference=result_id,
                        description=f"Execution step: {step.get('action', '')}",
                    )
                )

                hash_input = f"LOG_ATT:{result_id}"
                att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

                attachments.append(
                    Attachment(
                        attachment_id=f"ATT-{att_hash}",
                        attachment_type=AttachmentType.LOG,
                        content=str(step)[:500],
                        file_path=step.get("path"),
                    )
                )
                if len(references) >= 25:
                    break
            if len(references) >= 25:
                break

        return ExtractedEvidence(
            protocol_name="execution_protocol",
            references=tuple(references),
            attachments=tuple(attachments),
            raw_data=MappingProxyType({"record_count": len(records)}),
        )
