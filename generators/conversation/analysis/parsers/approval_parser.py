"""Approval parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from aiodoo_datasets.generators.conversation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.conversation.registries.parser_registry import ParserRegistry
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence
from aiodoo_datasets.generators.conversation.domain.reference import Reference


@ParserRegistry.register("approval_protocol")
class ApprovalParser(BaseParser):
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
