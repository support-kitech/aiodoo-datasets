"""Approval parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference


@ParserRegistry.register("approval_protocol")
class ApprovalParser(BaseParser):  # type: ignore[misc]
    """Parses Approval protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        for finding in data.get("findings", []):
            references.append(
                Reference(
                    source_generator="approval",
                    source_reference=finding.get("finding_id", "unknown"),
                    description=f"Approval finding: {finding.get('description', '')}",
                )
            )
        return ExtractedEvidence(
            protocol_name="approval_protocol",
            references=tuple(references),
            attachments=(),
            raw_data=MappingProxyType(data),
        )
